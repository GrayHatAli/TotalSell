import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def _seed_sale(client, headers):
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
    return r.json()["meta"]["id"]


def test_sales_report(client):
    headers = login(client)
    sale_id = _seed_sale(client, headers)
    resp = client.get("/api/v1/reports/sales?from_date=2026-01-01&to_date=2026-12-31", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["invoice_count"] >= 1


def test_purchase_report(client):
    headers = login(client)
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    prod = client.post("/api/v1/products", json={"name": "P1", "category_id": cat, "sale_price": 100, "cost_price": 60}, headers=headers).json()["meta"]["id"]
    sup = client.post("/api/v1/suppliers", json={"name": "Sup"}, headers=headers).json()["meta"]["id"]
    purchase = {
        "supplier_id": sup,
        "date": "2026-06-30T00:00:00",
        "items": [{"product_id": prod, "quantity": 2, "unit_cost": 50000}],
        "payment_method": "credit",
        "payment_status": "unpaid",
    }
    client.post("/api/v1/purchase-invoices", json=purchase, headers=headers)
    resp = client.get("/api/v1/reports/purchases?from_date=2026-01-01&to_date=2026-12-31", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["invoice_count"] >= 1


def test_inventory_report(client):
    headers = login(client)
    resp = client.get("/api/v1/reports/inventory", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert "items" in body["data"]


def test_invoice_pdf(client):
    headers = login(client)
    sale_id = _seed_sale(client, headers)
    resp = client.get(f"/api/v1/reports/invoices/{sale_id}/pdf?type=sale", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"


def test_report_excel(client):
    headers = login(client)
    _seed_sale(client, headers)
    resp = client.get("/api/v1/reports/sales/excel?from_date=2026-01-01&to_date=2026-12-31", headers=headers)
    assert resp.status_code == 200
    assert "spreadsheetml" in resp.headers["content-type"]
