from datetime import datetime

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    sku: str | None = Field(default=None, max_length=100)
    barcode: str | None = Field(default=None, max_length=100)
    category_id: int | None = Field(default=None, ge=1)
    product_type: str = Field(default="physical", max_length=20)
    unit: str | None = Field(default=None, max_length=50)
    cost_price: float | None = Field(default=None, ge=0)
    sale_price: float | None = Field(default=None, ge=0)
    min_stock: float | None = Field(default=None, ge=0)
    custom_attributes: dict | None = None
    active: bool = True


class ProductCreate(ProductBase):
    tag_ids: list[int] = Field(default_factory=list)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    sku: str | None = Field(default=None, max_length=100)
    barcode: str | None = Field(default=None, max_length=100)
    category_id: int | None = Field(default=None, ge=1)
    product_type: str | None = Field(default=None, max_length=20)
    unit: str | None = Field(default=None, max_length=50)
    cost_price: float | None = Field(default=None, ge=0)
    sale_price: float | None = Field(default=None, ge=0)
    min_stock: float | None = Field(default=None, ge=0)
    custom_attributes: dict | None = None
    active: bool | None = None
    tag_ids: list[int] | None = None


class ProductResponse(ProductBase):
    id: int
    category_name: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
