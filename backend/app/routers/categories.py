from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.common import ok
from app.services.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def list_categories(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(default=None),
    sort_by: str | None = Query(default="name"),
    sort_dir: str | None = Query(default="asc"),
):
    query = db.query(Category).filter(Category.deleted_at.is_(None))
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Category.name.ilike(like), Category.slug.ilike(like)))
    sort_col = getattr(Category, sort_by or "name", Category.name)
    query = query.order_by(sort_col.desc() if sort_dir == "desc" else sort_col.asc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok([CategoryResponse.model_validate(i).model_dump(mode="json") for i in items], meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    if payload.slug:
        exists = db.query(Category).filter(Category.slug == payload.slug, Category.deleted_at.is_(None)).first()
        if exists:
            raise HTTPException(status_code=400, detail="Slug already exists")
    if payload.parent_id is not None:
        parent = db.get(Category, payload.parent_id)
        if parent is None or parent.deleted_at is not None:
            raise HTTPException(status_code=400, detail="Parent category not found")
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return ok(CategoryResponse.model_validate(category).model_dump(mode="json"), meta={"id": category.id})


@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    category = db.get(Category, category_id)
    if category is None or category.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Category not found")
    return ok(CategoryResponse.model_validate(category).model_dump(mode="json"))


@router.patch("/{category_id}")
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    category = db.get(Category, category_id)
    if category is None or category.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Category not found")
    data = payload.model_dump(exclude_unset=True)
    if "slug" in data and data["slug"]:
        exists = db.query(Category).filter(Category.slug == data["slug"], Category.id != category_id, Category.deleted_at.is_(None)).first()
        if exists:
            raise HTTPException(status_code=400, detail="Slug already exists")
    if "parent_id" in data and data["parent_id"] is not None:
        if data["parent_id"] == category_id:
            raise HTTPException(status_code=400, detail="Cannot set category as its own parent")
        parent = db.get(Category, data["parent_id"])
        if parent is None or parent.deleted_at is not None:
            raise HTTPException(status_code=400, detail="Parent category not found")
    for key, value in data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return ok(CategoryResponse.model_validate(category).model_dump(mode="json"))


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    category = db.get(Category, category_id)
    if category is None or category.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Category not found")
    category.deleted_at = datetime.now(UTC)
    db.add(category)
    db.commit()
    return ok({"status": "deleted"})
