from pydantic import BaseModel


class LineItemBase(BaseModel):
    product_id: int | None = None
    quantity: float
    discount_pct: float = 0
    tax_pct: float = 0


class PurchaseItemCreate(LineItemBase):
    unit_cost: float


class PurchaseItemResponse(LineItemBase):
    id: int
    unit_cost: float
    line_total: float
    note: str | None = None

    model_config = {"from_attributes": True}


class SaleItemCreate(LineItemBase):
    unit_price: float


class SaleItemResponse(LineItemBase):
    id: int
    unit_price: float
    line_total: float
    unit_cost: float | None = None
    note: str | None = None

    model_config = {"from_attributes": True}
