from datetime import UTC, datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ok
from app.services.accounting import create_manual_journal_entry, create_reversal_entry, get_balance_sheet, get_general_ledger, get_profit_loss, get_trial_balance
from app.services.auth import get_current_user

router = APIRouter(prefix="/accounting", tags=["accounting"])


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.replace("Z", "+00:00")
    if len(value) > 10:
        return datetime.fromisoformat(value)
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC)


@router.post("/journal-entries")
def create_journal_entry(payload: dict, db: Session = Depends(get_db), _user = Depends(get_current_user)):
    payload["date"] = _parse_dt(payload.get("date")) or datetime.now(UTC)
    try:
        entry = create_manual_journal_entry(db, payload, user_id=getattr(_user, "id", None))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ok({"id": entry.id, "date": entry.date.isoformat(), "description": entry.description})


@router.post("/journal-entries/{entry_id}/reversal")
def reverse_journal_entry(entry_id: int, db: Session = Depends(get_db), _user = Depends(get_current_user)):
    """Correct a posted entry by creating a linked reversing entry (immutable history)."""
    try:
        entry = create_reversal_entry(db, entry_id, user_id=getattr(_user, "id", None))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ok({"id": entry.id, "reverses_entry_id": entry.reference_id, "description": entry.description})


@router.get("/journal-entries")
def list_journal_entries(db: Session = Depends(get_db), _user = Depends(get_current_user), account_id: int | None = None, from_date: str | None = None, to_date: str | None = None):
    ledger = get_general_ledger(db, account_id=account_id, from_date=_parse_dt(from_date), to_date=_parse_dt(to_date))
    return ok(ledger)


@router.get("/general-ledger")
def general_ledger(db: Session = Depends(get_db), _user = Depends(get_current_user), account_id: int | None = None, from_date: str | None = None, to_date: str | None = None):
    ledger = get_general_ledger(db, account_id=account_id, from_date=_parse_dt(from_date), to_date=_parse_dt(to_date))
    return ok(ledger)


@router.get("/trial-balance")
def trial_balance(db: Session = Depends(get_db), _user = Depends(get_current_user), date: str | None = None):
    as_of = _parse_dt(date)
    data = get_trial_balance(db, as_of)
    return ok(data)


@router.get("/profit-loss")
def profit_loss(db: Session = Depends(get_db), _user = Depends(get_current_user), from_date: str | None = None, to_date: str | None = None):
    if not from_date or not to_date:
        raise HTTPException(status_code=400, detail="from_date and to_date are required")
    f = _parse_dt(from_date)
    t = _parse_dt(to_date)
    data = get_profit_loss(db, f, t)
    return ok(data)


@router.get("/balance-sheet")
def balance_sheet(db: Session = Depends(get_db), _user = Depends(get_current_user), date: str | None = None):
    as_of = _parse_dt(date)
    data = get_balance_sheet(db, as_of)
    return ok(data)
