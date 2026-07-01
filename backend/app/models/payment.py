from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Payment(TimestampMixin, Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reference_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    reference_id: Mapped[int] = mapped_column(nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    method: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    bank_account_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    note: Mapped[str | None] = mapped_column(nullable=True)
