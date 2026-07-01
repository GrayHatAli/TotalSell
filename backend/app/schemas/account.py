from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    code: str
    name: str
    account_type: str
    parent_id: int | None = None
    is_active: bool

    model_config = {"from_attributes": True}
