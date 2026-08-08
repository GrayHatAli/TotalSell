from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.sale import SaleInvoice
from app.services.reports import _d
from app.schemas.common import ok
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("")
def list_customers(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(default=None),
    sort_by: str | None = Query(default="name"),
    sort_dir: str | None = Query(default="asc"),
):
    query = db.query(Customer).filter(Customer.deleted_at.is_(None))
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Customer.name.ilike(like), Customer.phone.ilike(like), Customer.email.ilike(like)))
    sort_col = getattr(Customer, sort_by, Customer.name)
    query = query.order_by(sort_col.desc() if sort_dir == "desc" else sort_col.asc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok([CustomerResponse.model_validate(i).model_dump(mode="json") for i in items], meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return ok(CustomerResponse.model_validate(customer).model_dump(mode="json"), meta={"id": customer.id})


@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    customer = db.get(Customer, customer_id)
    if customer is None or customer.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return ok(CustomerResponse.model_validate(customer).model_dump(mode="json"))


@router.get("/{customer_id}/statement")
def get_customer_statement(customer_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Get customer statement showing all invoices, payments, and outstanding balance"""
    customer = db.get(Customer, customer_id)
    if customer is None or customer.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get all sale invoices for this customer
    invoices = (db.query(SaleInvoice)
                .filter(SaleInvoice.customer_id == customer_id)
                .order_by(SaleInvoice.date.desc()).all())
    
    # Get all payments for this customer
    payments = (db.query(Payment)
                .filter(Payment.reference_type == "SALE", Payment.reference_id == customer_id)
                .order_by(Payment.date.desc()).all())
    
    # Calculate totals
    total_billed = sum(_d(inv.total) for inv in invoices)
    total_paid = sum(_d(p.amount) for p in payments)
    outstanding = float(total_billed - total_paid)
    
    return ok({
        "customer_id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "total_billed": float(total_billed),
        "total_paid": float(total_paid),
        "outstanding_balance": outstanding,
        "invoice_count": len(invoices),
        "payment_count": len(payments),
        "invoices": [SaleInvoice.model_validate(i).model_dump(mode="json") for i in invoices],
        "payments": [Payment.model_validate(p).model_dump(mode="json") for p in payments],
    })


@router.patch("/{customer_id}")
def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    customer = db.get(Customer, customer_id)
    if customer is None or customer.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Customer not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return ok(CustomerResponse.model_validate(customer).model_dump(mode="json"))


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    customer = db.get(Customer, customer_id)
    if customer is None or customer.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.deleted_at = datetime.now(UTC)
    db.add(customer)
    db.commit()
    return ok({"status": "deleted"})
