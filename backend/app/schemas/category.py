from datetime import datetime

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    parent_id: int | None = Field(default=None, ge=1)
    image_url: str | None = Field(default=None, max_length=500)
    active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    parent_id: int | None = Field(default=None, ge=1)
    image_url: str | None = Field(default=None, max_length=500)
    active: bool | None = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
