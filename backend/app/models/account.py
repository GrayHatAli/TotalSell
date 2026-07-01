from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Account(TimestampMixin, Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
