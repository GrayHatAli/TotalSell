from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.supplier import Supplier
from app.schemas.common import ok
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("")
def list_suppliers(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(default=None),
    sort_by: str | None = Query(default="name"),
    sort_dir: str | None = Query(default="asc"),
):
    query = db.query(Supplier).filter(Supplier.deleted_at.is_(None))
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Supplier.name.ilike(like), Supplier.phone.ilike(like), Supplier.email.ilike(like)))
    sort_col = getattr(Supplier, sort_by, Supplier.name)
    query = query.order_by(sort_col.desc() if sort_dir == "desc" else sort_col.asc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok([SupplierResponse.model_validate(i).model_dump(mode="json") for i in items], meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return ok(SupplierResponse.model_validate(supplier).model_dump(mode="json"), meta={"id": supplier.id})


@router.get("/{supplier_id}")
def get_supplier(supplier_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    supplier = db.get(Supplier, supplier_id)
    if supplier is None or supplier.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return ok(SupplierResponse.model_validate(supplier).model_dump(mode="json"))


@router.patch("/{supplier_id}")
def update_supplier(supplier_id: int, payload: SupplierUpdate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    supplier = db.get(Supplier, supplier_id)
    if supplier is None or supplier.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return ok(SupplierResponse.model_validate(supplier).model_dump(mode="json"))


@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    supplier = db.get(Supplier, supplier_id)
    if supplier is None or supplier.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier.deleted_at = datetime.now(UTC)
    db.add(supplier)
    db.commit()
    return ok({"status": "deleted"})
