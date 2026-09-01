from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment import Payment
from app.models.purchase import PurchaseInvoice
from app.services.reports import _d
from app.models.supplier import Supplier
from app.schemas.common import ok
from app.schemas.payment import PaymentResponse
from app.schemas.purchase import PurchaseInvoiceResponse
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


def _purchase_dict(invoice: PurchaseInvoice) -> dict:
    base = {c.name: getattr(invoice, c.name) for c in PurchaseInvoice.__table__.columns}
    return PurchaseInvoiceResponse(**base).model_dump(mode="json")


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
    sort_col = getattr(Supplier, sort_by or "name", Supplier.name)
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


@router.get("/{supplier_id}/statement")
def get_supplier_statement(supplier_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Get supplier statement showing all purchases and payments"""
    supplier = db.get(Supplier, supplier_id)
    if supplier is None or supplier.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Get all purchase invoices for this supplier
    purchases = (db.query(PurchaseInvoice)
                 .filter(PurchaseInvoice.supplier_id == supplier_id)
                 .order_by(PurchaseInvoice.date.desc()).all())
    
    # Get all payments for this supplier
    payments = (db.query(Payment)
                .filter(Payment.reference_type == "PURCHASE", Payment.reference_id == supplier_id)
                .order_by(Payment.date.desc()).all())
    
    # Calculate totals
    total_billed = sum(_d(inv.total) for inv in purchases)
    total_paid = sum(_d(p.amount) for p in payments)
    outstanding = float(total_billed - total_paid)
    
    return ok({
        "supplier_id": supplier.id,
        "name": supplier.name,
        "phone": supplier.phone,
        "email": supplier.email,
        "total_billed": float(total_billed),
        "total_paid": float(total_paid),
        "outstanding_balance": outstanding,
        "purchase_count": len(purchases),
        "payment_count": len(payments),
        "purchases": [_purchase_dict(i) for i in purchases],
        "payments": [PaymentResponse.model_validate(p).model_dump(mode="json") for p in payments],
    })


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
