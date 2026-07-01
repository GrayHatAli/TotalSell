import os
from datetime import UTC, datetime


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def _seed_invoice(client, headers):
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    prod = client.post("/api/v1/products", json={"name": "P1", "category_id": cat, "sale_price": 100, "cost_price": 60}, headers=headers).json()["meta"]["id"]
    cust = client.post("/api/v1/customers", json={"name": "Cust"}, headers=headers).json()["meta"]["id"]
    sale = {
        "customer_id": cust,
        "date": "2026-06-30T00:00:00",
        "items": [{"product_id": prod, "quantity": 2, "unit_price": 100000, "tax_pct": 9}],
        "payment_method": "cash",
        "payment_status": "paid",
    }
    r = client.post("/api/v1/sale-invoices", json=sale, headers=headers)
    assert r.status_code == 200
    return r.json()["data"]


def test_manual_journal_entry(client):
    headers = login(client)
    payload = {
        "date": "2026-06-30T00:00:00",
        "description": "Manual adjustment",
        "lines": [
            {"account_id": 1, "debit": 1000, "credit": 0},
            {"account_id": 2, "debit": 0, "credit": 1000},
        ],
    }
    resp = client.post("/api/v1/accounting/journal-entries", json=payload, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["id"] > 0


def test_manual_entry_rejects_unbalanced(client):
    headers = login(client)
    payload = {
        "date": "2026-06-30T00:00:00",
        "description": "Bad entry",
        "lines": [
            {"account_id": 1, "debit": 1000, "credit": 0},
            {"account_id": 2, "debit": 0, "credit": 500},
        ],
    }
    resp = client.post("/api/v1/accounting/journal-entries", json=payload, headers=headers)
    assert resp.status_code == 400


def test_trial_balance(client):
    headers = login(client)
    resp = client.get("/api/v1/accounting/trial-balance?date=2026-12-31", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_profit_loss(client):
    headers = login(client)
    resp = client.get("/api/v1/accounting/profit-loss?from_date=2026-01-01&to_date=2026-12-31", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["total_revenue"] >= 0


def test_balance_sheet(client):
    headers = login(client)
    resp = client.get("/api/v1/accounting/balance-sheet?date=2026-12-31", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["is_balanced"] is True


def test_general_ledger(client):
    headers = login(client)
    _seed_invoice(client, headers)
    resp = client.get("/api/v1/accounting/general-ledger", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert len(body["data"]) > 0
