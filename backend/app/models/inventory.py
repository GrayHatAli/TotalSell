from datetime import datetime
from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class InventoryMovement(TimestampMixin, Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(nullable=False, index=True)
    movement_type: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    quantity: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_id: Mapped[int | None] = mapped_column(nullable=True)
    note: Mapped[str | None] = mapped_column(nullable=True)
