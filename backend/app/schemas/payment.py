from datetime import datetime

from pydantic import BaseModel, Field


class PaymentBase(BaseModel):
    reference_type: str = Field(..., max_length=20)
    reference_id: int = Field(..., ge=1)
    amount: float = Field(..., gt=0)
    method: str = Field(..., max_length=20)
    bank_account_id: int | None = Field(default=None, ge=1)
    date: datetime
    note: str | None = None
    idempotency_key: str | None = Field(default=None, max_length=100)


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    journal_entry_id: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
