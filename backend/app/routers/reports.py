from datetime import UTC, datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ok
from app.services.auth import get_current_user
from app.services.reports import get_inventory_report, get_purchase_report, get_sales_report
from app.models.purchase import PurchaseInvoice
from app.models.sale import SaleInvoice

router = APIRouter(prefix="/reports", tags=["reports"])


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.replace("Z", "+00:00")
    if len(value) > 10:
        return datetime.fromisoformat(value)
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC)


@router.get("/sales")
def sales_report(db: Session = Depends(get_db), _user=Depends(get_current_user), from_date: str | None = None, to_date: str | None = None):
    if not from_date or not to_date:
        raise HTTPException(status_code=400, detail="from_date and to_date are required")
    f = _parse_dt(from_date)
    t = _parse_dt(to_date)
    if f is None or t is None:
        raise HTTPException(status_code=400, detail="Invalid date format")
    data = get_sales_report(db, f, t)
    return ok(data)


@router.get("/purchases")
def purchase_report(db: Session = Depends(get_db), _user=Depends(get_current_user), from_date: str | None = None, to_date: str | None = None):
    if not from_date or not to_date:
        raise HTTPException(status_code=400, detail="from_date and to_date are required")
    f = _parse_dt(from_date)
    t = _parse_dt(to_date)
    if f is None or t is None:
        raise HTTPException(status_code=400, detail="Invalid date format")
    data = get_purchase_report(db, f, t)
    return ok(data)


@router.get("/inventory")
def inventory_report(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    data = get_inventory_report(db)
    return ok(data)


@router.get("/invoices/{invoice_id}/pdf")
def invoice_pdf(invoice_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user), type: str = Query(default="sale", pattern="^(sale|purchase)$")):
    from weasyprint import HTML
    from app.models.customer import Customer
    from app.models.supplier import Supplier

    invoice: SaleInvoice | PurchaseInvoice
    party: Customer | Supplier | None = None
    if type == "sale":
        found = db.query(SaleInvoice).filter(SaleInvoice.id == invoice_id).first()
        if not found:
            raise HTTPException(status_code=404, detail="Invoice not found")
        invoice = found
        if invoice.customer_id:
            party = db.get(Customer, invoice.customer_id)
    else:
        found = db.query(PurchaseInvoice).filter(PurchaseInvoice.id == invoice_id).first()
        if not found:
            raise HTTPException(status_code=404, detail="Invoice not found")
        invoice = found
        if invoice.supplier_id:
            party = db.get(Supplier, invoice.supplier_id)

    html = f"""
    <html><body><h1>Invoice #{invoice.number}</h1>
    <p>Date: {invoice.date.strftime('%Y-%m-%d')}</p>
    <p>Party: {party.name if party else '—'}</p>
    <p>Total: {invoice.total}</p></body></html>
    """
    pdf = HTML(string=html).write_pdf()
    return Response(content=pdf, media_type="application/pdf")


@router.get("/{report_type}/excel")
def report_excel(report_type: str, db: Session = Depends(get_db), _user=Depends(get_current_user), from_date: str | None = None, to_date: str | None = None):
    from openpyxl import Workbook
    from io import BytesIO

    wb = Workbook()
    ws = wb.active if wb.active is not None else wb.create_sheet()
    ws.title = report_type.capitalize()

    if report_type == "sales":
        f = _parse_dt(from_date)
        t = _parse_dt(to_date)
        if not f or not t:
            raise HTTPException(status_code=400, detail="from_date and to_date are required")
        data = get_sales_report(db, f, t)
        ws.append(["Product", "Total", "Quantity"])
        for row in data["by_product"]:
            ws.append([row["name"], row["total"], row["quantity"]])
    elif report_type == "purchases":
        f = _parse_dt(from_date)
        t = _parse_dt(to_date)
        if not f or not t:
            raise HTTPException(status_code=400, detail="from_date and to_date are required")
        data = get_purchase_report(db, f, t)
        ws.append(["Supplier", "Total", "Count"])
        for row in data["by_supplier"]:
            ws.append([row["name"], row["total"], row["count"]])
    elif report_type == "inventory":
        data = get_inventory_report(db)
        ws.append(["Product", "SKU", "Stock", "Min Stock", "Low Stock"])
        for row in data["items"]:
            ws.append([row["name"], row["sku"], row["stock"], row["min_stock"], "Yes" if row["low_stock"] else "No"])
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return Response(content=buf.read(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
