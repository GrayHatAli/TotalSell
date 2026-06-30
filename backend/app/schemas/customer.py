from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CustomerBase(BaseModel):
    name: str = Field(..., max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=320)
    national_id: str | None = Field(default=None, max_length=100)
    customer_group: str | None = Field(default=None, max_length=100)
    credit_limit: float | None = Field(default=None, ge=0)
    address: str | None = None
    notes: str | None = None
    active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=320)
    national_id: str | None = Field(default=None, max_length=100)
    customer_group: str | None = Field(default=None, max_length=100)
    credit_limit: float | None = Field(default=None, ge=0)
    address: str | None = None
    notes: str | None = None
    active: bool | None = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
