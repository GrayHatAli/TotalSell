from datetime import datetime
from sqlalchemy import Boolean, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Supplier(TimestampMixin, Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    contact_person: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True, index=True)
    tax_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bank_account: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payment_terms: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
