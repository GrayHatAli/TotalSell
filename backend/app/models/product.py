from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sku: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    barcode: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    product_type: Mapped[str] = mapped_column(String(20), nullable=False, default="physical", index=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cost_price: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    sale_price: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True, index=True)
    min_stock: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    custom_attributes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    category: Mapped["Category | None"] = relationship("Category")
    tags: Mapped[list["Tag"]] = relationship(secondary="product_tags", back_populates="products")
