from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.models.product_tag import ProductTag
from app.models.tag import Tag
from app.schemas.common import ok
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    product_type: str | None = Query(default=None),
    active: bool | None = Query(default=None),
    sort_by: str | None = Query(default="name"),
    sort_dir: str | None = Query(default="asc"),
):
    query = db.query(Product).options(joinedload(Product.category), joinedload(Product.tags)).filter(Product.deleted_at.is_(None))
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Product.name.ilike(like), Product.sku.ilike(like), Product.barcode.ilike(like)))
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    if product_type is not None:
        query = query.filter(Product.product_type == product_type)
    if active is not None:
        query = query.filter(Product.active.is_(active))
    sort_col = getattr(Product, sort_by, Product.name)
    query = query.order_by(sort_col.desc() if sort_dir == "desc" else sort_col.asc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    results = []
    for item in items:
        data = ProductResponse.model_validate(item).model_dump(mode="json")
        data["category_name"] = item.category.name if item.category else None
        data["tags"] = [{"id": t.id, "name": t.name, "color": t.color} for t in item.tags]
        results.append(data)
    return ok(results, meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_product(payload: ProductCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    tag_ids = payload.tag_ids or []
    if payload.category_id is not None:
        category = db.get(Category, payload.category_id)
        if category is None or category.deleted_at is not None:
            raise HTTPException(status_code=400, detail="Category not found")
    if payload.sku:
        exists = db.query(Product).filter(Product.sku == payload.sku, Product.deleted_at.is_(None)).first()
        if exists:
            raise HTTPException(status_code=400, detail="SKU already exists")
    product_data = payload.model_dump(exclude={"tag_ids"})
    product = Product(**product_data)
    if tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        product.tags = tags
    db.add(product)
    db.commit()
    db.refresh(product)
    data = ProductResponse.model_validate(product).model_dump(mode="json")
    data["category_name"] = product.category.name if product.category else None
    data["tags"] = [{"id": t.id, "name": t.name, "color": t.color} for t in product.tags]
    return ok(data, meta={"id": product.id})


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    product = db.query(Product).options(joinedload(Product.category), joinedload(Product.tags)).get(product_id)
    if product is None or product.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Product not found")
    data = ProductResponse.model_validate(product).model_dump(mode="json")
    data["category_name"] = product.category.name if product.category else None
    data["tags"] = [{"id": t.id, "name": t.name, "color": t.color} for t in product.tags]
    return ok(data)


@router.patch("/{product_id}")
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    product = db.get(Product, product_id)
    if product is None or product.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Product not found")
    data = payload.model_dump(exclude_unset=True)
    tag_ids = data.pop("tag_ids", None)
    if "category_id" in data and data["category_id"] is not None:
        category = db.get(Category, data["category_id"])
        if category is None or category.deleted_at is not None:
            raise HTTPException(status_code=400, detail="Category not found")
    if "sku" in data and data["sku"]:
        exists = db.query(Product).filter(Product.sku == data["sku"], Product.id != product_id, Product.deleted_at.is_(None)).first()
        if exists:
            raise HTTPException(status_code=400, detail="SKU already exists")
    for key, value in data.items():
        setattr(product, key, value)
    if tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        product.tags = tags
    db.commit()
    db.refresh(product)
    resp = ProductResponse.model_validate(product).model_dump(mode="json")
    resp["category_name"] = product.category.name if product.category else None
    resp["tags"] = [{"id": t.id, "name": t.name, "color": t.color} for t in product.tags]
    return ok(resp)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    product = db.get(Product, product_id)
    if product is None or product.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.deleted_at = datetime.now(UTC)
    db.add(product)
    db.commit()
    return ok({"status": "deleted"})
