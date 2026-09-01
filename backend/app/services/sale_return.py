"""Sale return (credit note) workflow: reverses revenue, tax, settlement,
COGS, and restocks returned goods as a new FIFO cost layer."""
from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.inventory import InventoryLot, InventoryMovement, LotAllocation
from app.models.journal import JournalEntry, JournalLine
from app.models.product import Product
from app.models.sale import SaleInvoice, SaleItem, SaleReturn, SaleReturnItem
from app.models.user import AuditLog
from app.schemas.sale import SaleReturnCreate
from app.services.invoice import InvoiceError, _d, _get_account, _next_number, _round

Q = Decimal("0.01")


def _original_fifo_unit_cost(db: Session, invoice_id: int, product_id: int, fallback: Decimal) -> Decimal:
    """Average FIFO cost originally allocated to this invoice/product."""
    row = (
        db.query(
            func.sum(LotAllocation.quantity),
            func.sum(LotAllocation.quantity * LotAllocation.unit_cost),
        )
        .filter(
            LotAllocation.reference_type == "SALE_INVOICE",
            LotAllocation.reference_id == invoice_id,
            LotAllocation.product_id == product_id,
        )
        .one()
    )
    qty, cost = _d(row[0]), _d(row[1])
    if qty > 0:
        return _round(cost / qty)
    return fallback


def create_sale_return(
    db: Session, invoice_id: int, payload: SaleReturnCreate, user_id: int | None = None
) -> SaleReturn:
    invoice = db.get(SaleInvoice, invoice_id)
    if invoice is None:
        raise InvoiceError(f"Sale invoice {invoice_id} not found")

    sold: dict[int, Decimal] = {}
    for sale_item in db.query(SaleItem).filter(SaleItem.invoice_id == invoice_id).all():
        if sale_item.product_id is not None:
            sold[sale_item.product_id] = sold.get(sale_item.product_id, Decimal("0")) + _d(sale_item.quantity)

    returned_rows = (
        db.query(SaleReturnItem.product_id, func.sum(SaleReturnItem.quantity))
        .join(SaleReturn, SaleReturn.id == SaleReturnItem.return_id)
        .filter(SaleReturn.sale_invoice_id == invoice_id)
        .group_by(SaleReturnItem.product_id)
        .all()
    )
    returned: dict[int, Decimal] = {pid: _d(qty) for pid, qty in returned_rows}

    for item in payload.items:
        if item.product_id not in sold:
            raise InvoiceError(f"Product {item.product_id} is not on invoice {invoice.number}")
        available = sold[item.product_id] - returned.get(item.product_id, Decimal("0"))
        if _d(item.quantity) > available:
            raise InvoiceError(
                f"Cannot return more than sold for product {item.product_id}: "
                f"requested {_round(_d(item.quantity))}, returnable {_round(available)}"
            )

    return_date = payload.date or datetime.now(UTC)
    ret = SaleReturn(
        number=_next_number(db, "sale_return"),
        sale_invoice_id=invoice_id,
        date=return_date,
        reason=payload.reason,
        created_by=user_id,
    )
    db.add(ret)
    db.flush()

    subtotal = Decimal("0")
    tax_total = Decimal("0")
    cogs_total = Decimal("0")
    for item in payload.items:
        product_id = item.product_id
        qty = _d(item.quantity)
        sale_item = (
            db.query(SaleItem)
            .filter(SaleItem.invoice_id == invoice_id, SaleItem.product_id == product_id)
            .first()
        )
        if sale_item is None:
            raise InvoiceError(f"Product {product_id} is not on invoice {invoice.number}")
        price = _d(sale_item.unit_price)
        tax_pct = _d(sale_item.tax_pct)
        net = qty * price
        tax = _round(net * tax_pct / Decimal("100"))

        product = db.get(Product, product_id)
        unit_cost = Decimal("0")
        if product and product.product_type == "physical":
            unit_cost = _original_fifo_unit_cost(db, invoice_id, product_id, _d(sale_item.unit_cost) or Decimal("0"))
            cogs_total += _round(qty * unit_cost)
            # Restock returned goods as a new FIFO lot plus a traceability movement.
            db.add(
                InventoryLot(
                    product_id=product_id,
                    source_type="SALE_RETURN",
                    source_id=ret.id,
                    received_quantity=qty,
                    remaining_quantity=qty,
                    unit_cost=unit_cost,
                )
            )
            db.add(
                InventoryMovement(
                    product_id=product_id,
                    movement_type="IN",
                    quantity=qty,
                    unit_cost=unit_cost,
                    reference_type="SALE_RETURN",
                    reference_id=ret.id,
                    note=f"Sale return {ret.number}",
                )
            )

        subtotal += net
        tax_total += tax
        db.add(
            SaleReturnItem(
                return_id=ret.id,
                product_id=product_id,
                quantity=qty,
                unit_price=price,
                tax_pct=tax_pct,
                line_total=_round(net + tax),
                unit_cost=unit_cost,
            )
        )

    ret.subtotal = _round(subtotal)
    ret.tax_amount = tax_total
    ret.cogs_amount = _round(cogs_total)
    ret.total = _round(subtotal + tax_total)

    je = JournalEntry(
        date=ret.date,
        description=f"Sale return {ret.number}",
        reference_type="SALE_RETURN",
        reference_id=ret.id,
        created_by=user_id,
    )
    db.add(je)
    db.flush()

    # Reverse the revenue/tax/settlement legs of the original sale.
    if ret.subtotal > 0:
        revenue = _get_account(db, "4100")
        db.add(JournalLine(entry_id=je.id, account_id=revenue.id, debit=ret.subtotal, credit=Decimal("0")))
    if tax_total > 0:
        tax_payable = _get_account(db, "2120")
        db.add(JournalLine(entry_id=je.id, account_id=tax_payable.id, debit=tax_total, credit=Decimal("0")))
    if invoice.payment_method == "bank":
        settlement = _get_account(db, "1120")
    elif invoice.payment_method == "cash":
        settlement = _get_account(db, "1110")
    else:
        settlement = _get_account(db, "1130")
    db.add(JournalLine(entry_id=je.id, account_id=settlement.id, debit=Decimal("0"), credit=ret.total))

    # Reverse COGS at the original FIFO cost.
    if ret.cogs_amount > 0:
        inventory = _get_account(db, "1140")
        cogs = _get_account(db, "5100")
        db.add(JournalLine(entry_id=je.id, account_id=inventory.id, debit=ret.cogs_amount, credit=Decimal("0")))
        db.add(JournalLine(entry_id=je.id, account_id=cogs.id, debit=Decimal("0"), credit=ret.cogs_amount))

    ret.journal_entry_id = je.id

    db.add(
        AuditLog(
            actor_user_id=user_id,
            action="sale_return_created",
            details=(
                f"return_id={ret.id} number={ret.number} invoice_id={invoice_id} "
                f"total={ret.total} cogs={ret.cogs_amount}"
            ),
            created_at=datetime.now(UTC),
        )
    )
    db.commit()
    db.refresh(ret)
    return ret

