from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.bank_account import BankAccount
from app.models.inventory import InventoryMovement
from app.models.invoice_counter import InvoiceCounter
from app.models.journal import JournalEntry, JournalLine
from app.models.payment import Payment
from app.models.product import Product
from app.models.purchase import PurchaseInvoice, PurchaseItem
from app.models.sale import SaleInvoice, SaleItem

Q = Decimal("0.01")


def _d(v: Any) -> Decimal:
    return Decimal(str(v or 0))


def _round(v: Decimal) -> Decimal:
    return v.quantize(Q, rounding=ROUND_HALF_UP)


def _get_account(db: Session, code: str) -> Account:
    acc = db.query(Account).filter(Account.code == code).first()
    if acc is None:
        raise ValueError(f"Missing account code: {code}")
    return acc


def _next_number(db: Session, series: str) -> str:
    counter = db.query(InvoiceCounter).filter(InvoiceCounter.series == series).first()
    if counter is None:
        counter = InvoiceCounter(series=series, current_value=1)
        db.add(counter)
        next_val = 1
    else:
        next_val = counter.current_value + 1
        counter.current_value = next_val
    db.flush()
    prefix = "INV-P" if series == "purchase" else "INV-S"
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m')}-{next_val:04d}"


def create_purchase_invoice(db: Session, payload: dict, user_id: int | None = None) -> PurchaseInvoice:
    with db.begin_nested():
        number = _next_number(db, "purchase")
        items_data = payload.pop("items", [])
        invoice = PurchaseInvoice(number=number, created_by=user_id, **payload)
        db.add(invoice)
        db.flush()

        subtotal = Decimal("0")
        tax_total = Decimal("0")
        for item in items_data:
            qty = _d(item["quantity"])
            cost = _d(item["unit_cost"])
            discount_pct = _d(item.get("discount_pct", 0))
            tax_pct = _d(item.get("tax_pct", 0))
            line_before = qty * cost
            discount_amt = _round(line_before * discount_pct / Decimal("100"))
            line_total = _round((line_before - discount_amt) * (Decimal("1") + tax_pct / Decimal("100")))
            line_tax = _round(line_total - (line_before - discount_amt))
            subtotal += line_before - discount_amt
            tax_total += line_tax
            db.add(PurchaseItem(invoice_id=invoice.id, product_id=item.get("product_id"), quantity=float(qty), unit_cost=float(cost), discount_pct=float(discount_pct), tax_pct=float(tax_pct), line_total=float(line_total), note=item.get("note")))

            product = db.get(Product, item.get("product_id")) if item.get("product_id") else None
            if product and product.product_type == "physical":
                db.add(InventoryMovement(product_id=product.id, movement_type="IN", quantity=float(qty), unit_cost=float(cost), reference_type="PURCHASE_INVOICE", reference_id=invoice.id, note=f"Purchase invoice {number}"))

        discount_amount = _round(subtotal * _d(payload.get("discount_pct", 0)) / Decimal("100"))
        shipping = _d(payload.get("shipping", 0))
        invoice.subtotal = float(_round(subtotal))
        invoice.discount_amount = float(discount_amount)
        invoice.tax_amount = float(tax_total)
        invoice.shipping = float(shipping)
        invoice.total = float(_round(subtotal - discount_amount + tax_total + shipping))

        je = JournalEntry(date=invoice.date, description=f"Purchase invoice {number}", reference_type="PURCHASE_INVOICE", reference_id=invoice.id, created_by=user_id)
        db.add(je)
        db.flush()
        for item in items_data:
            qty = _d(item["quantity"])
            cost = _d(item["unit_cost"])
            line_tax = _round((qty * cost) * _d(item.get("tax_pct", 0)) / Decimal("100"))
            acc = _get_account(db, "1140")
            db.add(JournalLine(entry_id=je.id, account_id=acc.id, debit=float(qty * cost), credit=0))
            if line_tax > 0:
                acc_tax = _get_account(db, "1150")
                db.add(JournalLine(entry_id=je.id, account_id=acc_tax.id, debit=float(line_tax), credit=0))

        if invoice.payment_method == "bank":
            acc = _get_account(db, "1120")
        elif invoice.payment_method == "cash":
            acc = _get_account(db, "1110")
        else:
            acc = _get_account(db, "2110")
        db.add(JournalLine(entry_id=je.id, account_id=acc.id, debit=0, credit=float(invoice.total)))

        invoice.journal_entry_id = je.id
    db.commit()
    db.refresh(invoice)
    return invoice


def create_sale_invoice(db: Session, payload: dict, user_id: int | None = None) -> SaleInvoice:
    with db.begin_nested():
        number = _next_number(db, "sale")
        items_data = payload.pop("items", [])
        invoice = SaleInvoice(number=number, created_by=user_id, **payload)
        db.add(invoice)
        db.flush()

        subtotal = Decimal("0")
        tax_total = Decimal("0")
        total_cost = Decimal("0")
        for item in items_data:
            qty = _d(item["quantity"])
            price = _d(item["unit_price"])
            discount_pct = _d(item.get("discount_pct", 0))
            tax_pct = _d(item.get("tax_pct", 0))
            line_before = qty * price
            discount_amt = _round(line_before * discount_pct / Decimal("100"))
            line_total = _round((line_before - discount_amt) * (Decimal("1") + tax_pct / Decimal("100")))
            line_tax = _round(line_total - (line_before - discount_amt))
            subtotal += line_before - discount_amt
            tax_total += line_tax
            product = db.get(Product, item.get("product_id"))
            cost = _d(product.cost_price or 0) if product else Decimal("0")
            total_cost += qty * cost
            db.add(SaleItem(invoice_id=invoice.id, product_id=item.get("product_id"), quantity=float(qty), unit_price=float(price), discount_pct=float(discount_pct), tax_pct=float(tax_pct), line_total=float(line_total), unit_cost=float(cost), note=item.get("note")))

            if product and product.product_type == "physical":
                db.add(InventoryMovement(product_id=product.id, movement_type="OUT", quantity=float(qty), unit_cost=float(cost), reference_type="SALE_INVOICE", reference_id=invoice.id, note=f"Sale invoice {number}"))

        discount_amount = _round(subtotal * _d(payload.get("discount_pct", 0)) / Decimal("100"))
        invoice.subtotal = float(_round(subtotal))
        invoice.discount_amount = float(discount_amount)
        invoice.tax_amount = float(tax_total)
        invoice.total = float(_round(subtotal - discount_amount + tax_total))

        je = JournalEntry(date=invoice.date, description=f"Sale invoice {number}", reference_type="SALE_INVOICE", reference_id=invoice.id, created_by=user_id)
        db.add(je)
        db.flush()
        if invoice.payment_method == "bank":
            acc_recv = _get_account(db, "1120")
        elif invoice.payment_method == "cash":
            acc_recv = _get_account(db, "1110")
        else:
            acc_recv = _get_account(db, "1130")
        db.add(JournalLine(entry_id=je.id, account_id=acc_recv.id, debit=float(invoice.total), credit=0))

        acc_revenue = _get_account(db, "4100")
        db.add(JournalLine(entry_id=je.id, account_id=acc_revenue.id, debit=0, credit=float(_round(subtotal - discount_amount))))
        if tax_total > 0:
            acc_tax = _get_account(db, "2120")
            db.add(JournalLine(entry_id=je.id, account_id=acc_tax.id, debit=0, credit=float(tax_total)))

        cogs = _round(total_cost)
        if cogs > 0:
            acc_cogs = _get_account(db, "5100")
            acc_inv = _get_account(db, "1140")
            db.add(JournalLine(entry_id=je.id, account_id=acc_cogs.id, debit=float(cogs), credit=0))
            db.add(JournalLine(entry_id=je.id, account_id=acc_inv.id, debit=0, credit=float(cogs)))

        invoice.journal_entry_id = je.id
    db.commit()
    db.refresh(invoice)
    return invoice
