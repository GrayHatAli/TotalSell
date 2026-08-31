from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.customer import Customer
from app.models.inventory import InventoryLot, InventoryMovement, LotAllocation
from app.models.invoice_counter import InvoiceCounter
from app.models.journal import JournalEntry, JournalLine
from app.models.product import Product
from app.models.purchase import PurchaseInvoice, PurchaseItem
from app.models.sale import SaleInvoice, SaleItem
from app.models.supplier import Supplier
from app.models.user import AuditLog
from app.schemas.purchase import PurchaseInvoiceCreate
from app.schemas.sale import SaleInvoiceCreate

Q = Decimal("0.01")


class InvoiceError(ValueError):
    """Raised when an invoice cannot be posted. Routers map this to HTTP 422."""


def _d(v: Any) -> Decimal:
    if v is None:
        return Decimal("0")
    if isinstance(v, Decimal):
        return v
    return Decimal(str(v))


def _round(v: Decimal) -> Decimal:
    return v.quantize(Q, rounding=ROUND_HALF_UP)


def _get_account(db: Session, code: str) -> Account:
    acc = db.query(Account).filter(Account.code == code).first()
    if acc is None:
        raise InvoiceError(f"Missing account code: {code}")
    return acc


def _next_number(db: Session, series: str) -> str:
    """Generate the next invoice number.

    Uses a row lock (SELECT ... FOR UPDATE) on the counter row so concurrent
    PostgreSQL workers cannot allocate the same value. SQLite ignores the lock
    hint, which is acceptable for the local test suite.
    """
    prefix = {"purchase": "INV-P", "sale": "INV-S", "sale_return": "RET-S"}[series]
    year_month = datetime.now(UTC).strftime("%Y%m")

    counter = (
        db.query(InvoiceCounter)
        .filter(InvoiceCounter.series == series)
        .with_for_update()
        .first()
    )
    if counter is None:
        counter = InvoiceCounter(series=series, current_value=1)
        db.add(counter)
        next_value = 1
    else:
        counter.current_value += 1
        next_value = counter.current_value
    db.flush()

    return f"{prefix}-{year_month}-{next_value:04d}"


def _validate_active(db: Session, model, entity_id: int | None, label: str) -> None:
    if entity_id is None:
        return
    entity = db.get(model, entity_id)
    if entity is None:
        raise InvoiceError(f"{label} {entity_id} not found")
    if getattr(entity, "deleted_at", None) is not None or not getattr(entity, "active", True):
        raise InvoiceError(f"{label} {entity_id} is not active")


def _available_stock(db: Session, product_id: int) -> Decimal:
    """Available stock for a product: sum of FIFO lot remaining quantities.

    Lots are the authoritative cost layer / on-hand record; movements remain
    as traceability history.
    """
    total = (
        db.query(func.sum(InventoryLot.remaining_quantity))
        .filter(InventoryLot.product_id == product_id)
        .scalar()
    )
    return _d(total)


def _consume_lots_fifo(
    db: Session,
    product_id: int,
    quantity: Decimal,
    reference_type: str,
    reference_id: int | None,
) -> Decimal:
    """Consume ``quantity`` from the oldest lots (FIFO) and persist allocations.

    Returns the total FIFO cost of the consumed quantity. Raises
    ``InvoiceError`` when the available stock is insufficient, in which case
    nothing is mutated.
    """
    available = _available_stock(db, product_id)
    if quantity > available:
        raise InvoiceError(
            f"Insufficient stock for product {product_id}: "
            f"requested {_round(quantity)}, available {_round(available)}"
        )

    remaining = quantity
    total_cost = Decimal("0")
    lots = (
        db.query(InventoryLot)
        .filter(InventoryLot.product_id == product_id, InventoryLot.remaining_quantity > 0)
        .order_by(InventoryLot.id)
        .with_for_update()
        .all()
    )
    for lot in lots:
        if remaining <= 0:
            break
        take = min(_d(lot.remaining_quantity), remaining)
        lot.remaining_quantity = _d(lot.remaining_quantity) - take
        total_cost += take * _d(lot.unit_cost)
        db.add(
            LotAllocation(
                lot_id=lot.id,
                product_id=product_id,
                quantity=take,
                unit_cost=lot.unit_cost,
                reference_type=reference_type,
                reference_id=reference_id,
            )
        )
        remaining -= take
    return _round(total_cost)


def _check_sale_stock(db: Session, items: list[dict]) -> None:
    """Reject sales exceeding available stock for physical products.

    Quantities are aggregated per product so multi-line sales of the same
    product are validated against a single stock balance.
    """
    required: dict[int, Decimal] = {}
    for item in items:
        product_id = item.get("product_id")
        if product_id is None:
            continue
        product = db.get(Product, product_id)
        if product is None:
            raise InvoiceError(f"Product {product_id} not found")
        if product.deleted_at is not None or not product.active:
            raise InvoiceError(f"Product {product_id} is not active")
        if product.product_type != "physical":
            # Services and digital products intentionally bypass stock checks.
            continue
        required[product_id] = required.get(product_id, Decimal("0")) + _d(item["quantity"])

    for product_id, quantity in required.items():
        available = _available_stock(db, product_id)
        if quantity > available:
            raise InvoiceError(
                f"Insufficient stock for product {product_id}: "
                f"requested {_round(quantity)}, available {_round(available)}"
            )


def _compute_line(
    quantity: Decimal, rate: Decimal, discount_pct: Decimal, tax_pct: Decimal
) -> tuple[Decimal, Decimal, Decimal]:
    """Return (line_total, line_tax, net_amount) for a single invoice line."""
    line_before = quantity * rate
    discount_amt = _round(line_before * discount_pct / Decimal("100"))
    net = line_before - discount_amt
    line_total = _round(net * (Decimal("1") + tax_pct / Decimal("100")))
    line_tax = line_total - net
    return line_total, line_tax, net


def _line_data(item: Any, rate_field: str) -> dict:
    """Normalize a typed line item (Pydantic model) into a plain dict."""
    return {
        "product_id": item.product_id,
        "quantity": item.quantity,
        "rate": getattr(item, rate_field),
        "discount_pct": item.discount_pct,
        "tax_pct": item.tax_pct,
        "note": item.note,
    }


def _find_by_idempotency_key(db: Session, model, key: str | None):
    if not key:
        return None
    return db.query(model).filter(model.idempotency_key == key).first()


def _sale_invoice_data(db: Session, invoice: SaleInvoice, items: list[dict], user_id: int | None) -> None:
    """Validate, compute totals, create items/movements, and post the journal."""
    subtotal = Decimal("0")
    tax_total = Decimal("0")
    total_cost = Decimal("0")
    for item in items:
        qty = _d(item["quantity"])
        price = _d(item["rate"])
        line_total, line_tax, net = _compute_line(qty, price, _d(item["discount_pct"]), _d(item["tax_pct"]))
        subtotal += net
        tax_total += line_tax
        product = db.get(Product, item["product_id"]) if item["product_id"] else None
        line_cost = Decimal("0")
        if product and product.product_type == "physical":
            # FIFO: consume cost layers and persist the allocation so COGS is
            # reproducible later. Raises when stock is insufficient.
            line_cost = _consume_lots_fifo(db, product.id, qty, "SALE_INVOICE", invoice.id)
            db.add(
                InventoryMovement(
                    product_id=product.id,
                    movement_type="OUT",
                    quantity=qty,
                    unit_cost=_round(line_cost / qty) if qty > 0 else Decimal("0"),
                    reference_type="SALE_INVOICE",
                    reference_id=invoice.id,
                    note=f"Sale invoice {invoice.number}",
                )
            )
        total_cost += line_cost
        db.add(
            SaleItem(
                invoice_id=invoice.id,
                product_id=item["product_id"],
                quantity=qty,
                unit_price=price,
                discount_pct=_d(item["discount_pct"]),
                tax_pct=_d(item["tax_pct"]),
                line_total=line_total,
                unit_cost=_round(line_cost / qty) if qty > 0 else Decimal("0"),
                note=item["note"],
            )
        )

    discount_amount = _round(subtotal * _d(invoice.discount_pct) / Decimal("100"))
    invoice.subtotal = _round(subtotal)
    invoice.discount_amount = discount_amount
    invoice.tax_amount = tax_total
    invoice.total = _round(subtotal - discount_amount + tax_total)

    je = JournalEntry(
        date=invoice.date,
        description=f"Sale invoice {invoice.number}",
        reference_type="SALE_INVOICE",
        reference_id=invoice.id,
        created_by=user_id,
    )
    db.add(je)
    db.flush()
    if invoice.payment_method == "bank":
        acc_recv = _get_account(db, "1120")
    elif invoice.payment_method == "cash":
        acc_recv = _get_account(db, "1110")
    else:
        acc_recv = _get_account(db, "1130")
    db.add(JournalLine(entry_id=je.id, account_id=acc_recv.id, debit=invoice.total, credit=Decimal("0")))

    acc_revenue = _get_account(db, "4100")
    db.add(
        JournalLine(
            entry_id=je.id,
            account_id=acc_revenue.id,
            debit=Decimal("0"),
            credit=_round(subtotal - discount_amount),
        )
    )
    if tax_total > 0:
        acc_tax = _get_account(db, "2120")
        db.add(JournalLine(entry_id=je.id, account_id=acc_tax.id, debit=Decimal("0"), credit=tax_total))

    cogs = _round(total_cost)
    if cogs > 0:
        acc_cogs = _get_account(db, "5100")
        acc_inv = _get_account(db, "1140")
        db.add(JournalLine(entry_id=je.id, account_id=acc_cogs.id, debit=cogs, credit=Decimal("0")))
        db.add(JournalLine(entry_id=je.id, account_id=acc_inv.id, debit=Decimal("0"), credit=cogs))

    invoice.journal_entry_id = je.id


def _purchase_invoice_data(db: Session, invoice: PurchaseInvoice, items: list[dict], user_id: int | None) -> None:
    """Validate, compute totals, create items/movements, and post the journal."""
    subtotal = Decimal("0")
    tax_total = Decimal("0")
    for item in items:
        qty = _d(item["quantity"])
        cost = _d(item["rate"])
        line_total, line_tax, net = _compute_line(qty, cost, _d(item["discount_pct"]), _d(item["tax_pct"]))
        subtotal += net
        tax_total += line_tax
        db.add(
            PurchaseItem(
                invoice_id=invoice.id,
                product_id=item["product_id"],
                quantity=qty,
                unit_cost=cost,
                discount_pct=_d(item["discount_pct"]),
                tax_pct=_d(item["tax_pct"]),
                line_total=line_total,
                note=item["note"],
            )
        )

        product = db.get(Product, item["product_id"]) if item["product_id"] else None
        if product and product.product_type == "physical":
            # Create a FIFO cost layer for the received quantity.
            db.add(
                InventoryLot(
                    product_id=product.id,
                    source_type="PURCHASE_INVOICE",
                    source_id=invoice.id,
                    received_quantity=qty,
                    remaining_quantity=qty,
                    unit_cost=cost,
                )
            )
            db.add(
                InventoryMovement(
                    product_id=product.id,
                    movement_type="IN",
                    quantity=qty,
                    unit_cost=cost,
                    reference_type="PURCHASE_INVOICE",
                    reference_id=invoice.id,
                    note=f"Purchase invoice {invoice.number}",
                )
            )

    discount_amount = _round(subtotal * _d(invoice.discount_pct) / Decimal("100"))
    shipping = _d(invoice.shipping)
    invoice.subtotal = _round(subtotal)
    invoice.discount_amount = discount_amount
    invoice.tax_amount = tax_total
    invoice.total = _round(subtotal - discount_amount + tax_total + shipping)

    je = JournalEntry(
        date=invoice.date,
        description=f"Purchase invoice {invoice.number}",
        reference_type="PURCHASE_INVOICE",
        reference_id=invoice.id,
        created_by=user_id,
    )
    db.add(je)
    db.flush()
    for item in items:
        qty = _d(item["quantity"])
        cost = _d(item["rate"])
        acc = _get_account(db, "1140")
        db.add(JournalLine(entry_id=je.id, account_id=acc.id, debit=qty * cost, credit=Decimal("0")))
        line_tax = _round(qty * cost * _d(item["tax_pct"]) / Decimal("100"))
        if line_tax > 0:
            acc_tax = _get_account(db, "1150")
            db.add(JournalLine(entry_id=je.id, account_id=acc_tax.id, debit=line_tax, credit=Decimal("0")))

    if invoice.payment_method == "bank":
        acc = _get_account(db, "1120")
    elif invoice.payment_method == "cash":
        acc = _get_account(db, "1110")
    else:
        acc = _get_account(db, "2110")
    db.add(JournalLine(entry_id=je.id, account_id=acc.id, debit=Decimal("0"), credit=invoice.total))

    invoice.journal_entry_id = je.id


def create_purchase_invoice(db: Session, payload: PurchaseInvoiceCreate, user_id: int | None = None) -> PurchaseInvoice:
    """Create a purchase invoice as a single atomic transaction on the injected session."""
    existing = _find_by_idempotency_key(db, PurchaseInvoice, payload.idempotency_key)
    if existing is not None:
        return existing

    _validate_active(db, Supplier, payload.supplier_id, "Supplier")

    invoice_data = payload.model_dump(exclude={"items"})
    items_data = [_line_data(item, "unit_cost") for item in payload.items]

    invoice = PurchaseInvoice(number=_next_number(db, "purchase"), created_by=user_id, **invoice_data)
    db.add(invoice)
    db.flush()

    _purchase_invoice_data(db, invoice, items_data, user_id)

    db.add(
        AuditLog(
            actor_user_id=user_id,
            action="purchase_invoice_created",
            details=f"invoice_id={invoice.id} number={invoice.number} total={invoice.total}",
            created_at=datetime.now(UTC),
        )
    )
    db.commit()
    db.refresh(invoice)
    return invoice


def create_sale_invoice(db: Session, payload: SaleInvoiceCreate, user_id: int | None = None) -> SaleInvoice:
    """Create a sale invoice as a single atomic transaction on the injected session."""
    existing = _find_by_idempotency_key(db, SaleInvoice, payload.idempotency_key)
    if existing is not None:
        return existing

    _validate_active(db, Customer, payload.customer_id, "Customer")

    items_data = [_line_data(item, "unit_price") for item in payload.items]
    _check_sale_stock(db, items_data)

    invoice_data = payload.model_dump(exclude={"items"})
    invoice = SaleInvoice(number=_next_number(db, "sale"), created_by=user_id, **invoice_data)
    db.add(invoice)
    db.flush()

    _sale_invoice_data(db, invoice, items_data, user_id)

    db.add(
        AuditLog(
            actor_user_id=user_id,
            action="sale_invoice_created",
            details=f"invoice_id={invoice.id} number={invoice.number} total={invoice.total}",
            created_at=datetime.now(UTC),
        )
    )
    db.commit()
    db.refresh(invoice)
    return invoice


