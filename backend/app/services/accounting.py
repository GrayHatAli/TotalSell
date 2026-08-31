from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.journal import JournalEntry, JournalLine
from app.models.user import AuditLog

Q = Decimal("0.01")


def _d(v: Any) -> Decimal:
    return Decimal(str(v or 0))


def _round(v: Decimal) -> Decimal:
    return v.quantize(Q, rounding=ROUND_HALF_UP)


def create_manual_journal_entry(db: Session, payload: dict, user_id: int | None = None) -> JournalEntry:
    lines_data = payload.pop("lines", [])
    total_debit = sum(_d(line.get("debit", 0)) for line in lines_data)
    total_credit = sum(_d(line.get("credit", 0)) for line in lines_data)
    if total_debit != total_credit:
        raise ValueError(f"Debits ({total_debit}) do not equal credits ({total_credit})")

    entry = JournalEntry(date=payload["date"], description=payload.get("description"), reference_type="MANUAL", reference_id=None, created_by=user_id)
    db.add(entry)
    db.flush()

    for line in lines_data:
        db.add(JournalLine(entry_id=entry.id, account_id=line["account_id"], debit=float(_d(line.get("debit", 0))), credit=float(_d(line.get("credit", 0))), note=line.get("note")))

    db.commit()
    db.refresh(entry)
    return entry


def create_reversal_entry(db: Session, entry_id: int, user_id: int | None = None, reason: str | None = None) -> JournalEntry:
    """Create a reversing journal entry for a posted entry.

    Posted entries are immutable: corrections are made by reversing entries
    with debits and credits swapped, linked back to the original entry.
    """
    original = db.get(JournalEntry, entry_id)
    if original is None:
        raise ValueError(f"Journal entry {entry_id} not found")

    existing = (
        db.query(JournalEntry)
        .filter(JournalEntry.reference_type == "REVERSAL", JournalEntry.reference_id == entry_id)
        .first()
    )
    if existing is not None:
        raise ValueError(f"Journal entry {entry_id} has already been reversed by entry {existing.id}")

    lines = db.query(JournalLine).filter(JournalLine.entry_id == entry_id).all()
    if not lines:
        raise ValueError(f"Journal entry {entry_id} has no lines")

    reversal = JournalEntry(
        date=original.date,
        description=f"Reversal of entry {entry_id}" + (f": {reason}" if reason else ""),
        reference_type="REVERSAL",
        reference_id=entry_id,
        created_by=user_id,
    )
    db.add(reversal)
    db.flush()
    for line in lines:
        db.add(
            JournalLine(
                entry_id=reversal.id,
                account_id=line.account_id,
                debit=line.credit,
                credit=line.debit,
                note=reason or line.note,
            )
        )
    db.add(
        AuditLog(
            actor_user_id=user_id,
            action="journal_entry_reversed",
            details=f"reversal_entry_id={reversal.id} original_entry_id={entry_id}",
            created_at=datetime.now(UTC),
        )
    )
    db.commit()
    db.refresh(reversal)
    return reversal


def get_trial_balance(db: Session, as_of_date: datetime | None = None) -> list[dict]:
    query = db.query(
        Account.id,
        Account.code,
        Account.name,
        func.coalesce(func.sum(JournalLine.debit), 0).label("total_debit"),
        func.coalesce(func.sum(JournalLine.credit), 0).label("total_credit"),
    ).join(JournalLine, JournalLine.account_id == Account.id).join(JournalEntry, JournalEntry.id == JournalLine.entry_id)

    if as_of_date:
        query = query.filter(JournalEntry.date <= as_of_date)
    else:
        query = query.filter(JournalEntry.date <= datetime.now(UTC))

    query = query.filter(Account.is_active.is_(True)).group_by(Account.id, Account.code, Account.name).order_by(Account.code)
    results = []
    for row in query.all():
        balance = float(row.total_debit) - float(row.total_credit)
        results.append({
            "account_id": row.id,
            "code": row.code,
            "name": row.name,
            "debit": float(row.total_debit),
            "credit": float(row.total_credit),
            "balance": balance,
        })
    return results


def get_profit_loss(db: Session, from_date: datetime, to_date: datetime) -> dict:
    revenue_query = db.query(func.coalesce(func.sum(JournalLine.credit), 0)).join(JournalEntry, JournalEntry.id == JournalLine.entry_id).join(Account, Account.id == JournalLine.account_id).filter(Account.account_type == "REVENUE").filter(JournalEntry.date >= from_date).filter(JournalEntry.date <= to_date)
    total_revenue = float(revenue_query.scalar() or 0)

    expense_query = db.query(func.coalesce(func.sum(JournalLine.debit), 0)).join(JournalEntry, JournalEntry.id == JournalLine.entry_id).join(Account, Account.id == JournalLine.account_id).filter(Account.account_type == "EXPENSE").filter(JournalEntry.date >= from_date).filter(JournalEntry.date <= to_date)
    total_expenses = float(expense_query.scalar() or 0)

    net_profit = total_revenue - total_expenses
    return {"total_revenue": total_revenue, "total_expenses": total_expenses, "net_profit": net_profit, "from_date": from_date.isoformat(), "to_date": to_date.isoformat()}


def get_balance_sheet(db: Session, as_of_date: datetime | None = None) -> dict:
    base_filter = JournalEntry.date <= (as_of_date or datetime.now(UTC))

    asset_query = (db.query(func.coalesce(func.sum(JournalLine.debit - JournalLine.credit), 0))
                   .join(Account, Account.id == JournalLine.account_id)
                   .join(JournalEntry, JournalEntry.id == JournalLine.entry_id)
                   .filter(Account.account_type == "ASSET")
                   .filter(base_filter))
    total_assets = float(asset_query.scalar() or 0)

    liability_query = (db.query(func.coalesce(func.sum(JournalLine.credit - JournalLine.debit), 0))
                       .join(Account, Account.id == JournalLine.account_id)
                       .join(JournalEntry, JournalEntry.id == JournalLine.entry_id)
                       .filter(Account.account_type == "LIABILITY")
                       .filter(base_filter))
    total_liabilities = float(liability_query.scalar() or 0)

    equity_query = (db.query(func.coalesce(func.sum(JournalLine.credit - JournalLine.debit), 0))
                    .join(Account, Account.id == JournalLine.account_id)
                    .join(JournalEntry, JournalEntry.id == JournalLine.entry_id)
                    .filter(Account.account_type == "EQUITY")
                    .filter(base_filter))
    total_equity = float(equity_query.scalar() or 0)

    return {
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "liabilities_plus_equity": total_liabilities + total_equity,
        "is_balanced": abs(total_assets - (total_liabilities + total_equity)) < 0.01,
        "as_of_date": (as_of_date or datetime.now(UTC)).isoformat(),
    }


def get_general_ledger(db: Session, account_id: int | None = None, from_date: datetime | None = None, to_date: datetime | None = None) -> list[dict]:
    query = db.query(JournalLine, JournalEntry, Account).join(JournalEntry, JournalEntry.id == JournalLine.entry_id).join(Account, Account.id == JournalLine.account_id)
    if account_id is not None:
        query = query.filter(JournalLine.account_id == account_id)
    if from_date:
        query = query.filter(JournalEntry.date >= from_date)
    if to_date:
        query = query.filter(JournalEntry.date <= to_date)
    query = query.order_by(JournalEntry.date, JournalEntry.id)

    results = []
    for line, entry, account in query.all():
        results.append({
            "entry_id": entry.id,
            "date": entry.date.isoformat() if entry.date else None,
            "description": entry.description,
            "reference_type": entry.reference_type,
            "reference_id": entry.reference_id,
            "account_id": account.id,
            "account_code": account.code,
            "account_name": account.name,
            "debit": float(line.debit),
            "credit": float(line.credit),
            "note": line.note,
        })
    return results
