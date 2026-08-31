import os
import threading
from decimal import Decimal

import pytest

from app.database import SessionLocal
from app.models.inventory import InventoryLot
from app.models.journal import JournalEntry, JournalLine
from app.models.payment import Payment
from app.models.purchase import PurchaseInvoice
from app.models.sale import SaleInvoice
from app.models.user import AuditLog


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def _seed(client, headers, product_type="physical"):
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    prod = client.post(
        "/api/v1/products",
        json={"name": "P1", "category_id": cat, "sale_price": 100, "cost_price": 60, "product_type": product_type},
        headers=headers,
    ).json()["meta"]["id"]
    sup = client.post("/api/v1/suppliers", json={"name": "Sup"}, headers=headers).json()["meta"]["id"]
    cust = client.post("/api/v1/customers", json={"name": "Cust"}, headers=headers).json()["meta"]["id"]
    return prod, sup, cust


def _purchase_payload(product_id, supplier_id, quantity=5, unit_cost=50000):
    return {
        "supplier_id": supplier_id,
        "date": "2026-06-29T00:00:00",
        "items": [{"product_id": product_id, "quantity": quantity, "unit_cost": unit_cost}],
        "payment_method": "credit",
        "payment_status": "unpaid",
    }


def _sale_payload(product_id, customer_id, quantity=2, unit_price=100000):
    return {
        "customer_id": customer_id,
        "date": "2026-06-30T00:00:00",
        "items": [{"product_id": product_id, "quantity": quantity, "unit_price": unit_price}],
        "payment_method": "credit",
        "payment_status": "unpaid",
    }


def test_sale_invoice_idempotency_key(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    resp = client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup), headers=headers)
    assert resp.status_code == 200

    payload = _sale_payload(prod, cust)
    payload["idempotency_key"] = "sale-key-1"
    first = client.post("/api/v1/sale-invoices", json=payload, headers=headers)
    assert first.status_code == 200
    first_id = first.json()["meta"]["id"]

    retry = client.post("/api/v1/sale-invoices", json=payload, headers=headers)
    assert retry.status_code == 200
    assert retry.json()["meta"]["id"] == first_id

    db = SessionLocal()
    try:
        assert db.query(SaleInvoice).count() == 1
    finally:
        db.close()


def test_purchase_invoice_idempotency_key(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)

    payload = _purchase_payload(prod, sup)
    payload["idempotency_key"] = "purchase-key-1"
    first = client.post("/api/v1/purchase-invoices", json=payload, headers=headers)
    assert first.status_code == 200
    first_id = first.json()["meta"]["id"]

    retry = client.post("/api/v1/purchase-invoices", json=payload, headers=headers)
    assert retry.status_code == 200
    assert retry.json()["meta"]["id"] == first_id

    db = SessionLocal()
    try:
        assert db.query(PurchaseInvoice).count() == 1
    finally:
        db.close()


def test_sale_rejects_insufficient_stock(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)

    resp = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust), headers=headers)
    assert resp.status_code == 422
    assert "Insufficient stock" in resp.json()["error"]["message"]


def test_sale_allows_partial_stock_and_rejects_excess(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    resp = client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=3), headers=headers)
    assert resp.status_code == 200

    ok = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust, quantity=3), headers=headers)
    assert ok.status_code == 200

    excess = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust, quantity=1), headers=headers)
    assert excess.status_code == 422


def test_service_product_bypasses_stock_check(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers, product_type="service")

    resp = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust), headers=headers)
    assert resp.status_code == 200


def test_payment_posts_journal_and_updates_status(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup), headers=headers)
    sale_resp = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust), headers=headers)
    inv_id = sale_resp.json()["meta"]["id"]
    total = sale_resp.json()["data"]["total"]

    # Partial payment.
    partial_payload = {
        "reference_type": "SALE",
        "reference_id": inv_id,
        "amount": total / 2,
        "method": "cash",
        "date": "2026-07-01T00:00:00",
    }
    partial = client.post("/api/v1/payments", json=partial_payload, headers=headers)
    assert partial.status_code == 200
    assert partial.json()["data"]["journal_entry_id"] is not None

    detail = client.get(f"/api/v1/sale-invoices/{inv_id}", headers=headers)
    assert detail.json()["data"]["payment_status"] == "partial"

    # Settle the remainder.
    settle_payload = dict(partial_payload, amount=total - total / 2)
    settle = client.post("/api/v1/payments", json=settle_payload, headers=headers)
    assert settle.status_code == 200

    detail = client.get(f"/api/v1/sale-invoices/{inv_id}", headers=headers)
    assert detail.json()["data"]["payment_status"] == "paid"

    # Every payment journal entry must balance exactly.
    db = SessionLocal()
    try:
        entries = db.query(JournalEntry).filter(JournalEntry.reference_type == "PAYMENT").all()
        assert len(entries) == 2
        for entry in entries:
            lines = db.query(JournalLine).filter(JournalLine.entry_id == entry.id).all()
            assert sum(l.debit for l in lines) == sum(l.credit for l in lines)
    finally:
        db.close()


def test_payment_rejects_overpayment(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup), headers=headers)
    sale_resp = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust), headers=headers)
    inv_id = sale_resp.json()["meta"]["id"]
    total = sale_resp.json()["data"]["total"]

    payload = {
        "reference_type": "SALE",
        "reference_id": inv_id,
        "amount": total + 1,
        "method": "cash",
        "date": "2026-07-01T00:00:00",
    }
    resp = client.post("/api/v1/payments", json=payload, headers=headers)
    assert resp.status_code == 422
    assert "remaining" in resp.json()["error"]["message"]


def test_payment_idempotency_key(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup), headers=headers)
    sale_resp = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust), headers=headers)
    inv_id = sale_resp.json()["meta"]["id"]

    payload = {
        "reference_type": "SALE",
        "reference_id": inv_id,
        "amount": 50000,
        "method": "cash",
        "date": "2026-07-01T00:00:00",
        "idempotency_key": "payment-key-1",
    }
    first = client.post("/api/v1/payments", json=payload, headers=headers)
    assert first.status_code == 200
    first_id = first.json()["meta"]["id"]

    retry = client.post("/api/v1/payments", json=payload, headers=headers)
    assert retry.status_code == 200
    assert retry.json()["meta"]["id"] == first_id

    db = SessionLocal()
    try:
        assert db.query(Payment).count() == 1
    finally:
        db.close()


def test_payment_idempotency_via_header(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup), headers=headers)
    sale_resp = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust), headers=headers)
    inv_id = sale_resp.json()["meta"]["id"]

    payload = {
        "reference_type": "SALE",
        "reference_id": inv_id,
        "amount": 50000,
        "method": "cash",
        "date": "2026-07-01T00:00:00",
    }
    hdrs = dict(headers, **{"Idempotency-Key": "header-key-1"})
    first = client.post("/api/v1/payments", json=payload, headers=hdrs)
    assert first.status_code == 200
    first_id = first.json()["meta"]["id"]

    retry = client.post("/api/v1/payments", json=payload, headers=hdrs)
    assert retry.status_code == 200
    assert retry.json()["meta"]["id"] == first_id


def test_inventory_adjustment_endpoint(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=4), headers=headers)

    # Controlled adjustment with a reason is accepted and audited.
    resp = client.post(
        "/api/v1/inventory-movements/adjustments",
        json={"product_id": prod, "quantity": 1, "unit_cost": 50000, "reason": "Damaged in warehouse"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["movement_type"] == "ADJ"

    # Adjustment cannot exceed available stock (4 purchased, 1 already adjusted).
    excess = client.post(
        "/api/v1/inventory-movements/adjustments",
        json={"product_id": prod, "quantity": 4, "unit_cost": 50000, "reason": "Count correction"},
        headers=headers,
    )
    assert excess.status_code == 422

    # Reason is mandatory.
    missing_reason = client.post(
        "/api/v1/inventory-movements/adjustments",
        json={"product_id": prod, "quantity": 1, "unit_cost": 50000},
        headers=headers,
    )
    assert missing_reason.status_code == 422


def test_invoice_journal_entries_balance(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup), headers=headers)
    sale_resp = client.post(
        "/api/v1/sale-invoices",
        json=_sale_payload(prod, cust, quantity=3, unit_price=100000),
        headers=headers,
    )
    assert sale_resp.status_code == 200

    db = SessionLocal()
    try:
        for ref_type in ("SALE_INVOICE", "PURCHASE_INVOICE"):
            entries = db.query(JournalEntry).filter(JournalEntry.reference_type == ref_type).all()
            assert len(entries) >= 1
            for entry in entries:
                lines = db.query(JournalLine).filter(JournalLine.entry_id == entry.id).all()
                assert sum(l.debit for l in lines) == sum(l.credit for l in lines)
    finally:
        db.close()


def _cogs_debit(invoice_id: int) -> Decimal:
    """Total COGS debited for a sale invoice's journal entry."""
    from app.models.account import Account

    db = SessionLocal()
    try:
        lines = (
            db.query(JournalLine)
            .join(JournalEntry, JournalEntry.id == JournalLine.entry_id)
            .filter(JournalEntry.reference_type == "SALE_INVOICE", JournalEntry.reference_id == invoice_id)
            .all()
        )
        cogs = db.query(Account).filter(Account.code == "5100").one()
        return sum(Decimal(str(l.debit)) for l in lines if l.account_id == cogs.id)
    finally:
        db.close()


def test_fifo_cogs_multiple_cost_layers(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)

    # Layer 1: 2 units @ 40. Layer 2: 2 units @ 60.
    assert client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=2, unit_cost=40), headers=headers).status_code == 200
    assert client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=2, unit_cost=60), headers=headers).status_code == 200

    sale = client.post(
        "/api/v1/sale-invoices",
        json={**_sale_payload(prod, cust, quantity=3), "payment_method": "credit", "payment_status": "unpaid"},
        headers=headers,
    )
    assert sale.status_code == 200
    inv_id = sale.json()["meta"]["id"]

    # FIFO COGS = 2*40 + 1*60 = 140, not 3 * current cost_price.
    assert _cogs_debit(inv_id) == Decimal("140")


def test_fifo_partial_consumption_and_stock(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=5, unit_cost=10), headers=headers)

    assert client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust, quantity=2), headers=headers).status_code == 200
    db = SessionLocal()
    try:
        lot = db.query(InventoryLot).filter(InventoryLot.product_id == prod).one()
        assert Decimal(str(lot.remaining_quantity)) == Decimal("3")
    finally:
        db.close()

    assert client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust, quantity=3), headers=headers).status_code == 200
    # Stock is exhausted; a further sale must fail and create nothing.
    exhausted = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust, quantity=1), headers=headers)
    assert exhausted.status_code == 422
    db = SessionLocal()
    try:
        assert db.query(SaleInvoice).count() == 2
    finally:
        db.close()


def test_sale_return_reverses_and_restocks(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=3, unit_cost=50), headers=headers)
    sale = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust, quantity=2), headers=headers)
    inv_id = sale.json()["meta"]["id"]

    ret = client.post(
        f"/api/v1/sale-invoices/{inv_id}/returns",
        json={"items": [{"product_id": prod, "quantity": 1}], "reason": "Defective unit"},
        headers=headers,
    )
    assert ret.status_code == 200
    body = ret.json()["data"]
    assert body["number"].startswith("RET-S")
    assert body["cogs_amount"] == 50
    assert body["journal_entry_id"] is not None

    # Restocked: 3 purchased - 2 sold + 1 returned = 2 on hand.
    db = SessionLocal()
    try:
        remaining = sum(
            Decimal(str(l.remaining_quantity))
            for l in db.query(InventoryLot).filter(InventoryLot.product_id == prod).all()
        )
        assert remaining == Decimal("2")

        entry = db.query(JournalEntry).filter(JournalEntry.id == body["journal_entry_id"]).one()
        lines = db.query(JournalLine).filter(JournalLine.entry_id == entry.id).all()
        assert sum(Decimal(str(l.debit)) for l in lines) == sum(Decimal(str(l.credit)) for l in lines)
    finally:
        db.close()

    # Return history is listed per invoice.
    listed = client.get(f"/api/v1/sale-invoices/{inv_id}/returns", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()["data"]) == 1


def test_sale_return_cannot_exceed_sold(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=5), headers=headers)
    sale = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust, quantity=2), headers=headers)
    inv_id = sale.json()["meta"]["id"]

    payload = {"items": [{"product_id": prod, "quantity": 2}]}
    assert client.post(f"/api/v1/sale-invoices/{inv_id}/returns", json=payload, headers=headers).status_code == 200
    again = client.post(f"/api/v1/sale-invoices/{inv_id}/returns", json=payload, headers=headers)
    assert again.status_code == 422
    assert "returnable" in again.json()["error"]["message"]


def test_journal_reversal_endpoint(client):
    headers = login(client)
    payload = {
        "date": "2026-06-30T00:00:00",
        "description": "Manual entry to reverse",
        "lines": [
            {"account_id": 1, "debit": 1000, "credit": 0},
            {"account_id": 2, "debit": 0, "credit": 1000},
        ],
    }
    created = client.post("/api/v1/accounting/journal-entries", json=payload, headers=headers)
    entry_id = created.json()["data"]["id"]

    reversal = client.post(f"/api/v1/accounting/journal-entries/{entry_id}/reversal", headers=headers)
    assert reversal.status_code == 200
    reversal_id = reversal.json()["data"]["id"]
    assert reversal.json()["data"]["reverses_entry_id"] == entry_id

    # The reversal must exactly offset the original.
    db = SessionLocal()
    try:
        original_lines = {
            l.account_id: (Decimal(str(l.debit)), Decimal(str(l.credit)))
            for l in db.query(JournalLine).filter(JournalLine.entry_id == entry_id).all()
        }
        reversal_lines = {
            l.account_id: (Decimal(str(l.debit)), Decimal(str(l.credit)))
            for l in db.query(JournalLine).filter(JournalLine.entry_id == reversal_id).all()
        }
        for account_id, (debit, credit) in original_lines.items():
            assert reversal_lines[account_id] == (credit, debit)
    finally:
        db.close()

    # A second reversal of the same entry is rejected.
    duplicate = client.post(f"/api/v1/accounting/journal-entries/{entry_id}/reversal", headers=headers)
    assert duplicate.status_code == 400


def test_audit_log_covers_financial_writes(client):
    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup), headers=headers)
    sale = client.post("/api/v1/sale-invoices", json=_sale_payload(prod, cust), headers=headers)
    inv_id = sale.json()["meta"]["id"]
    client.post(
        "/api/v1/payments",
        json={"reference_type": "SALE", "reference_id": inv_id, "amount": 100000, "method": "cash", "date": "2026-07-01T00:00:00"},
        headers=headers,
    )
    client.post(
        "/api/v1/inventory-movements/adjustments",
        json={"product_id": prod, "quantity": 1, "unit_cost": 50000, "reason": "Damaged in warehouse"},
        headers=headers,
    )

    db = SessionLocal()
    try:
        actions = {a.action for a in db.query(AuditLog).all()}
    finally:
        db.close()
    assert {"purchase_invoice_created", "sale_invoice_created", "payment_posted", "inventory_adjustment"} <= actions


def test_concurrent_invoice_creation_postgres(client):
    """Concurrent creations must allocate unique numbers (PostgreSQL row lock).

    Skipped on SQLite, which does not implement SELECT ... FOR UPDATE.
    """
    if not os.environ.get("DATABASE_URL", "").startswith("postgresql"):
        pytest.skip("Requires PostgreSQL (row-lock semantics)")

    headers = login(client)
    prod, sup, cust = _seed(client, headers)
    client.post("/api/v1/purchase-invoices", json=_purchase_payload(prod, sup, quantity=10), headers=headers)

    from app.schemas.sale import SaleInvoiceCreate, SaleItemCreate
    from app.services.invoice import create_sale_invoice

    numbers: list[str] = []
    errors: list[Exception] = []

    def worker():
        db = SessionLocal()
        try:
            payload = SaleInvoiceCreate(
                customer_id=cust,
                date="2026-06-30T00:00:00",
                items=[SaleItemCreate(product_id=prod, quantity=1, unit_price=100000)],
                payment_method="credit",
            )
            invoice = create_sale_invoice(db, payload)
            numbers.append(invoice.number)
        except Exception as exc:  # surfaced through the assertions below
            errors.append(exc)
        finally:
            db.close()

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    assert len(numbers) == len(set(numbers)), f"Duplicate invoice numbers: {numbers}"





