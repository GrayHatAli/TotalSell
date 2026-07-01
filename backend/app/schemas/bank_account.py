from datetime import datetime

from pydantic import BaseModel, Field


class BankAccountBase(BaseModel):
    name: str = Field(..., max_length=255)
    account_type: str = Field(default="bank", max_length=50)
    iban: str | None = Field(default=None, max_length=34)
    account_number: str | None = Field(default=None, max_length=50)
    bank_name: str | None = Field(default=None, max_length=255)
    opening_balance: float = Field(default=0, ge=0)
    notes: str | None = None
    active: bool = True


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    account_type: str | None = Field(default=None, max_length=50)
    iban: str | None = Field(default=None, max_length=34)
    account_number: str | None = Field(default=None, max_length=50)
    bank_name: str | None = Field(default=None, max_length=255)
    opening_balance: float | None = Field(default=None, ge=0)
    notes: str | None = None
    active: bool | None = None


class BankAccountResponse(BankAccountBase):
    id: int
    current_balance: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
