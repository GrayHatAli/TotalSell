from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sale import SaleInvoice, SaleItem
from app.schemas.common import ok
from app.schemas.invoice import SaleItemResponse
from app.schemas.sale import SaleInvoiceCreate, SaleInvoiceResponse
from app.services.auth import get_current_user
from app.services.invoice import create_sale_invoice

router = APIRouter(prefix="/sale-invoices", tags=["sale-invoices"])


def _to_response(invoice: SaleInvoice) -> dict:
    base = {c.name: getattr(invoice, c.name) for c in SaleInvoice.__table__.columns}
    data = SaleInvoiceResponse(**base).model_dump(mode="json")
    data["items"] = [SaleItemResponse.model_validate(i).model_dump(mode="json") for i in invoice.items]
    return data


@router.get("")
def list_sale_invoices(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    customer_id: int | None = None,
    payment_status: str | None = None,
):
    query = db.query(SaleInvoice)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(SaleInvoice.number.ilike(like), SaleInvoice.reference_number.ilike(like)))
    if customer_id is not None:
        query = query.filter(SaleInvoice.customer_id == customer_id)
    if payment_status is not None:
        query = query.filter(SaleInvoice.payment_status == payment_status)
    query = query.order_by(SaleInvoice.date.desc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    results = []
    for inv in items:
        results.append(_to_response(inv))
    return ok(results, meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_sale_invoice_endpoint(payload: SaleInvoiceCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    invoice = create_sale_invoice(db, payload.model_dump(), user_id=getattr(_user, "id", None))
    data = _to_response(invoice)
    data["items"] = []
    return ok(data, meta={"id": invoice.id})


@router.get("/{invoice_id}")
def get_sale_invoice(invoice_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    invoice = db.get(SaleInvoice, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Sale invoice not found")
    return ok(_to_response(invoice))
