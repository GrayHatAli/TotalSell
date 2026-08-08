from datetime import datetime

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., max_length=100)
    color: str | None = Field(default=None, max_length=20)


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    """Only allow updating name and color, with name uniqueness check"""
    name: str | None = Field(default=None, max_length=100)
    color: str | None = None


class TagResponse(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
