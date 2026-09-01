from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class BankAccount(TimestampMixin, Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False, default="bank", index=True)
    iban: Mapped[str | None] = mapped_column(String(34), nullable=True)
    account_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    current_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
