from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.supplier import Supplier
    from app.models.user import User


class PurchaseInvoice(TimestampMixin, Base):
    __tablename__ = "purchase_invoices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False, index=True)
    reference_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    discount_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tax_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    shipping: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    payment_method: Mapped[str | None] = mapped_column(String(20), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False, default="unpaid", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    journal_entry_id: Mapped[int | None] = mapped_column(ForeignKey("journal_entries.id"), nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True, index=True)

    items: Mapped[list["PurchaseItem"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")
    supplier: Mapped["Supplier"] = relationship(backref="purchase_invoices")
    created_by_user: Mapped["User | None"] = relationship("User", foreign_keys=[created_by])


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("purchase_invoices.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    discount_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    tax_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    line_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    invoice: Mapped[PurchaseInvoice] = relationship(back_populates="items")
    product: Mapped["Product | None"] = relationship("Product")
