from datetime import datetime

from pydantic import BaseModel, Field


class SupplierBase(BaseModel):
    name: str = Field(..., max_length=255)
    contact_person: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=320)
    tax_id: str | None = Field(default=None, max_length=100)
    bank_account: str | None = Field(default=None, max_length=255)
    payment_terms: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    contact_person: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=320)
    tax_id: str | None = Field(default=None, max_length=100)
    bank_account: str | None = Field(default=None, max_length=255)
    payment_terms: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    active: bool | None = None


class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
