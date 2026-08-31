from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.bank_account import BankAccount
from app.models.journal import JournalEntry, JournalLine
from app.models.payment import Payment
from app.models.purchase import PurchaseInvoice
from app.models.sale import SaleInvoice
from app.models.user import AuditLog
from app.schemas.payment import PaymentCreate

Q = Decimal("0.01")

# Canonical account codes used for posting (must match app/seed.py).
CASH_ACCOUNT = "1110"
BANK_ACCOUNT = "1120"
ACCOUNTS_RECEIVABLE = "1130"
ACCOUNTS_PAYABLE = "2110"

SUPPORTED_REFERENCE_TYPES: dict[str, type] = {
    "SALE": SaleInvoice,
    "PURCHASE": PurchaseInvoice,
}


class PaymentError(ValueError):
    """Raised when a payment cannot be posted. Routers map this to HTTP 422."""


def _get_account(db: Session, code: str) -> Account:
    acc = db.query(Account).filter(Account.code == code).first()
    if acc is None:
        raise PaymentError(f"Missing account code: {code}")
    return acc


def _settled_amount(db: Session, reference_type: str, reference_id: int) -> Decimal:
    total = (
        db.query(func.sum(Payment.amount))
        .filter(Payment.reference_type == reference_type, Payment.reference_id == reference_id)
        .scalar()
    )
    return Decimal(str(total or 0))


def create_payment(db: Session, payload: PaymentCreate, user_id: int | None = None) -> Payment:
    """Post a payment as a single atomic transaction.

    Creates the payment record, a balanced journal entry, and updates the
    invoice balance/status. A retried idempotency key returns the original
    payment without duplicating any effect.
    """
    if payload.idempotency_key:
        existing = db.query(Payment).filter(Payment.idempotency_key == payload.idempotency_key).first()
        if existing is not None:
            return existing

    reference_type = (payload.reference_type or "").upper()
    model = SUPPORTED_REFERENCE_TYPES.get(reference_type)
    if model is None:
        raise PaymentError(f"Unsupported payment reference_type: {payload.reference_type}")

    invoice = db.get(model, payload.reference_id)
    if invoice is None:
        raise PaymentError(f"{reference_type.title()} invoice {payload.reference_id} not found")

    if payload.method not in ("cash", "bank"):
        raise PaymentError("Payment method must be 'cash' or 'bank'")

    if payload.method == "bank" and payload.bank_account_id is not None:
        bank_account = db.get(BankAccount, payload.bank_account_id)
        if bank_account is None or bank_account.deleted_at is not None or not bank_account.active:
            raise PaymentError(f"Bank account {payload.bank_account_id} is not active")

    amount = Decimal(str(payload.amount)).quantize(Q, rounding=ROUND_HALF_UP)
    if amount <= 0:
        raise PaymentError("Payment amount must be positive")

    paid = _settled_amount(db, reference_type, payload.reference_id)
    remaining = Decimal(str(invoice.total)) - paid
    if amount > remaining:
        raise PaymentError(
            f"Payment exceeds remaining invoice balance: amount {amount}, remaining {remaining.quantize(Q)}"
        )

    if payload.method == "bank":
        settlement = _get_account(db, BANK_ACCOUNT)
    else:
        settlement = _get_account(db, CASH_ACCOUNT)

    je = JournalEntry(
        date=payload.date,
        description=f"Payment for {reference_type.lower()} invoice {payload.reference_id}",
        reference_type="PAYMENT",
        created_by=user_id,
    )
    db.add(je)
    db.flush()

    if reference_type == "SALE":
        # Settle accounts receivable: debit cash/bank, credit AR.
        counter_account = _get_account(db, ACCOUNTS_RECEIVABLE)
        db.add(JournalLine(entry_id=je.id, account_id=settlement.id, debit=amount, credit=Decimal("0")))
        db.add(JournalLine(entry_id=je.id, account_id=counter_account.id, debit=Decimal("0"), credit=amount))
    else:
        # Settle accounts payable: debit AP, credit cash/bank.
        counter_account = _get_account(db, ACCOUNTS_PAYABLE)
        db.add(JournalLine(entry_id=je.id, account_id=counter_account.id, debit=amount, credit=Decimal("0")))
        db.add(JournalLine(entry_id=je.id, account_id=settlement.id, debit=Decimal("0"), credit=amount))

    payment = Payment(
        reference_type=reference_type,
        reference_id=payload.reference_id,
        amount=amount,
        method=payload.method,
        bank_account_id=payload.bank_account_id,
        date=payload.date,
        note=payload.note,
        idempotency_key=payload.idempotency_key,
        journal_entry_id=je.id,
    )
    db.add(payment)
    db.flush()

    invoice.payment_status = "paid" if paid + amount >= Decimal(str(invoice.total)) else "partial"

    db.add(
        AuditLog(
            actor_user_id=user_id,
            action="payment_posted",
            details=(
                f"payment_id={payment.id} reference_type={reference_type} "
                f"reference_id={payload.reference_id} amount={amount} journal_entry_id={je.id}"
            ),
            created_at=payload.date,
        )
    )
    db.commit()
    db.refresh(payment)
    return payment
