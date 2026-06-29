from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models.user import AuditLog, User
from app.security import hash_password


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


def main() -> None:
    db = SessionLocal()
    try:
        seed_admin(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()

