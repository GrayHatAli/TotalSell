from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
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
