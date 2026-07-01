from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.customer import Customer
from app.models.inventory import InventoryMovement
from app.models.product import Product
from app.models.purchase import PurchaseInvoice, PurchaseItem
from app.models.sale import SaleInvoice, SaleItem
from app.models.supplier import Supplier


def _d(v: Any) -> Decimal:
    return Decimal(str(v or 0))


def get_sales_report(db: Session, from_date: datetime, to_date: datetime) -> dict:
    query = db.query(SaleInvoice).filter(SaleInvoice.date >= from_date).filter(SaleInvoice.date <= to_date)
    invoices = query.order_by(SaleInvoice.date.desc()).all()

    total_revenue = sum(_d(inv.total) for inv in invoices)
    by_customer: dict[int, dict] = {}
    by_product: dict[int, dict] = {}

    for inv in invoices:
        cust_id = inv.customer_id or 0
        by_customer.setdefault(cust_id, {"name": "Walk-in", "total": Decimal("0"), "count": 0})
        if cust_id:
            customer = db.get(Customer, cust_id)
            if customer:
                by_customer[cust_id]["name"] = customer.name
        by_customer[cust_id]["total"] += _d(inv.total)
        by_customer[cust_id]["count"] += 1

        for item in inv.items:
            pid = item.product_id or 0
            by_product.setdefault(pid, {"name": "Unknown", "total": Decimal("0"), "qty": Decimal("0")})
            product = db.get(Product, pid) if pid else None
            if product:
                by_product[pid]["name"] = product.name
            by_product[pid]["total"] += _d(item.line_total)
            by_product[pid]["qty"] += _d(item.quantity)

    return {
        "total_revenue": float(total_revenue),
        "invoice_count": len(invoices),
        "from_date": from_date.isoformat(),
        "to_date": to_date.isoformat(),
        "by_customer": [
            {"customer_id": k, "name": v["name"], "total": float(v["total"]), "count": v["count"]}
            for k, v in sorted(by_customer.items(), key=lambda x: x[1]["total"], reverse=True)
        ],
        "by_product": [
            {"product_id": k, "name": v["name"], "total": float(v["total"]), "quantity": float(v["qty"])}
            for k, v in sorted(by_product.items(), key=lambda x: x[1]["total"], reverse=True)
        ],
    }


def get_purchase_report(db: Session, from_date: datetime, to_date: datetime) -> dict:
    query = db.query(PurchaseInvoice).filter(PurchaseInvoice.date >= from_date).filter(PurchaseInvoice.date <= to_date)
    invoices = query.order_by(PurchaseInvoice.date.desc()).all()

    total_purchases = sum(_d(inv.total) for inv in invoices)
    by_supplier: dict[int, dict] = {}

    for inv in invoices:
        sid = inv.supplier_id or 0
        by_supplier.setdefault(sid, {"name": "Unknown", "total": Decimal("0"), "count": 0})
        supplier = db.get(Supplier, sid)
        if supplier:
            by_supplier[sid]["name"] = supplier.name
        by_supplier[sid]["total"] += _d(inv.total)
        by_supplier[sid]["count"] += 1

    return {
        "total_purchases": float(total_purchases),
        "invoice_count": len(invoices),
        "from_date": from_date.isoformat(),
        "to_date": to_date.isoformat(),
        "by_supplier": [
            {"supplier_id": k, "name": v["name"], "total": float(v["total"]), "count": v["count"]}
            for k, v in sorted(by_supplier.items(), key=lambda x: x[1]["total"], reverse=True)
        ],
    }


def get_inventory_report(db: Session) -> dict:
    products = db.query(Product).filter(Product.deleted_at.is_(None)).all()
    items = []
    for p in products:
        movements = db.query(InventoryMovement).filter(InventoryMovement.product_id == p.id).all()
        in_qty = sum(_d(m.quantity) for m in movements if m.movement_type == "IN")
        out_qty = sum(_d(m.quantity) for m in movements if m.movement_type == "OUT")
        stock = float(in_qty - out_qty)
        items.append({
            "product_id": p.id,
            "name": p.name,
            "sku": p.sku,
            "category": p.category.name if p.category else None,
            "stock": stock,
            "min_stock": float(_d(p.min_stock)),
            "cost_price": float(_d(p.cost_price)),
            "sale_price": float(_d(p.sale_price)),
            "low_stock": p.min_stock is not None and stock < float(_d(p.min_stock)),
        })
    return {"items": items, "low_stock_count": sum(1 for i in items if i["low_stock"])}
