from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.purchase import PurchaseInvoice, PurchaseItem
from app.schemas.common import ok
from app.schemas.invoice import PurchaseItemResponse
from app.schemas.purchase import PurchaseInvoiceCreate, PurchaseInvoiceResponse
from app.services.auth import get_current_user
from app.services.invoice import create_purchase_invoice

router = APIRouter(prefix="/purchase-invoices", tags=["purchase-invoices"])


def _to_response(invoice: PurchaseInvoice) -> dict:
    base = {c.name: getattr(invoice, c.name) for c in PurchaseInvoice.__table__.columns}
    data = PurchaseInvoiceResponse(**base).model_dump(mode="json")
    data["items"] = [PurchaseItemResponse.model_validate(i).model_dump(mode="json") for i in invoice.items]
    return data


@router.get("")
def list_purchase_invoices(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    supplier_id: int | None = None,
    payment_status: str | None = None,
):
    query = db.query(PurchaseInvoice)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(PurchaseInvoice.number.ilike(like), PurchaseInvoice.reference_number.ilike(like)))
    if supplier_id is not None:
        query = query.filter(PurchaseInvoice.supplier_id == supplier_id)
    if payment_status is not None:
        query = query.filter(PurchaseInvoice.payment_status == payment_status)
    query = query.order_by(PurchaseInvoice.date.desc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    results = []
    for inv in items:
        results.append(_to_response(inv))
    return ok(results, meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_purchase_invoice_endpoint(
    payload: PurchaseInvoiceCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if idempotency_key and not payload.idempotency_key:
        payload.idempotency_key = idempotency_key
    try:
        invoice = create_purchase_invoice(db, payload, user_id=getattr(_user, "id", None))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    data = _to_response(invoice)
    data["items"] = []
    return ok(data, meta={"id": invoice.id})


@router.get("/{invoice_id}")
def get_purchase_invoice(invoice_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    invoice = db.get(PurchaseInvoice, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Purchase invoice not found")
    return ok(_to_response(invoice))
