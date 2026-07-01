from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models.account import Account
from app.models.user import AuditLog, User
from app.security import hash_password

DEFAULT_ACCOUNTS = [
    ("1110", "Cash", "ASSET"),
    ("1120", "Bank Accounts", "ASSET"),
    ("1130", "Accounts Receivable", "ASSET"),
    ("1140", "Inventory", "ASSET"),
    ("1150", "Tax Receivable", "ASSET"),
    ("2110", "Accounts Payable", "LIABILITY"),
    ("2120", "Tax Payable", "LIABILITY"),
    ("3100", "Owner's Equity", "EQUITY"),
    ("3200", "Retained Earnings", "EQUITY"),
    ("4100", "Sales Revenue", "REVENUE"),
    ("5100", "Cost of Goods Sold", "EXPENSE"),
    ("5200", "Operating Expenses", "EXPENSE"),
]


def seed_admin(db: Session) -> None:
    settings = get_settings()
    existing = db.query(User).filter(User.email == settings.admin_email).one_or_none()
    if existing is not None:
        return

    user = User(
        email=settings.admin_email,
        password_hash=hash_password(settings.admin_password),
        is_active=True,
        is_admin=True,
    )
    db.add(user)
    db.flush()
    db.add(AuditLog(actor_user_id=user.id, action="admin_seeded", details="Initial admin user created", created_at=datetime.now(UTC)))
    db.commit()


def seed_accounts(db: Session) -> None:
    for code, name, account_type in DEFAULT_ACCOUNTS:
        exists = db.query(Account).filter(Account.code == code).first()
        if exists is None:
            db.add(Account(code=code, name=name, account_type=account_type, is_active=True))
    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        seed_admin(db)
        seed_accounts(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
