from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment import Payment
from app.schemas.common import ok
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.auth import get_current_user
from app.services.payment import create_payment as create_payment_service

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("")
def list_payments(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    reference_type: str | None = None,
    reference_id: int | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    query = db.query(Payment)
    if reference_type is not None:
        query = query.filter(Payment.reference_type == reference_type)
    if reference_id is not None:
        query = query.filter(Payment.reference_id == reference_id)
    query = query.order_by(desc(Payment.date))
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok([PaymentResponse.model_validate(i).model_dump(mode="json") for i in items], meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if idempotency_key and not payload.idempotency_key:
        payload.idempotency_key = idempotency_key
    try:
        payment = create_payment_service(db, payload, user_id=getattr(_user, "id", None))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ok(PaymentResponse.model_validate(payment).model_dump(mode="json"), meta={"id": payment.id})
