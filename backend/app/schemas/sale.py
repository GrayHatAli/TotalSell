from datetime import datetime

from pydantic import BaseModel, Field


class SaleInvoiceBase(BaseModel):
    customer_id: int | None = Field(default=None, ge=1)
    date: datetime
    reference_number: str | None = Field(default=None, max_length=100)
    discount_pct: float = Field(default=0, ge=0, le=100)
    tax_pct: float = Field(default=0, ge=0, le=100)
    payment_method: str | None = Field(default=None, max_length=20)
    payment_status: str = Field(default="unpaid", max_length=20)
    notes: str | None = None


class SaleInvoiceCreate(SaleInvoiceBase):
    items: list[dict] = Field(default_factory=list, min_length=1)


class SaleInvoiceResponse(SaleInvoiceBase):
    id: int
    number: str
    subtotal: float
    discount_amount: float
    tax_amount: float
    total: float
    created_by: int | None = None
    journal_entry_id: int | None = None
    created_at: datetime
    updated_at: datetime
    items: list[dict] | None = None

    model_config = {"from_attributes": True}
