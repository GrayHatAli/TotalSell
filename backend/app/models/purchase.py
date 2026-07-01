from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class PurchaseInvoice(TimestampMixin, Base):
    __tablename__ = "purchase_invoices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    supplier_id: Mapped[int] = mapped_column(nullable=False, index=True)
    reference_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    subtotal: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    discount_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tax_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    tax_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    shipping: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    payment_method: Mapped[str | None] = mapped_column(String(20), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False, default="unpaid", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int | None] = mapped_column(nullable=True)
    journal_entry_id: Mapped[int | None] = mapped_column(nullable=True)

    items: Mapped[list["PurchaseItem"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("purchase_invoices.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    quantity: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    tax_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    line_total: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    invoice: Mapped[PurchaseInvoice] = relationship(back_populates="items")
