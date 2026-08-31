from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.invoice import SaleItemCreate


class SaleInvoiceBase(BaseModel):
    customer_id: int | None = Field(default=None, ge=1)
    date: datetime
    reference_number: str | None = Field(default=None, max_length=100)
    discount_pct: float = Field(default=0, ge=0, le=100)
    tax_pct: float = Field(default=0, ge=0, le=100)
    payment_method: str | None = Field(default=None, max_length=20)
    payment_status: str = Field(default="unpaid", max_length=20)
    notes: str | None = None
    idempotency_key: str | None = Field(default=None, max_length=100)


class SaleReturnItemCreate(BaseModel):
    product_id: int = Field(..., ge=1)
    quantity: float = Field(..., gt=0)


class SaleReturnCreate(BaseModel):
    date: datetime | None = None
    reason: str | None = Field(default=None, max_length=1000)
    items: list[SaleReturnItemCreate] = Field(..., min_length=1)


class SaleReturnItemResponse(BaseModel):
    id: int
    product_id: int | None = None
    quantity: float
    unit_price: float
    tax_pct: float
    line_total: float
    unit_cost: float | None = None

    model_config = {"from_attributes": True}


class SaleReturnResponse(BaseModel):
    id: int
    number: str
    sale_invoice_id: int
    date: datetime
    reason: str | None = None
    subtotal: float
    tax_amount: float
    cogs_amount: float
    total: float
    journal_entry_id: int | None = None
    created_at: datetime
    items: list[SaleReturnItemResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class SaleInvoiceCreate(SaleInvoiceBase):
    items: list[SaleItemCreate] = Field(default_factory=list, min_length=1)


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
