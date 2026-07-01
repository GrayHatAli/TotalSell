from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class InvoiceCounter(Base):
    __tablename__ = "invoice_counters"

    series: Mapped[str] = mapped_column(String(20), primary_key=True)
    current_value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
