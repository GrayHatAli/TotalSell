import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def _seed_product(client, headers):
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    return cat, client.post("/api/v1/products", json={"name": "P1", "category_id": cat, "sale_price": 100, "cost_price": 60}, headers=headers).json()["meta"]["id"]


def _seed_supplier(client, headers):
    return client.post("/api/v1/suppliers", json={"name": "Sup"}, headers=headers).json()["meta"]["id"]


def _seed_customer(client, headers):
    return client.post("/api/v1/customers", json={"name": "Cust"}, headers=headers).json()["meta"]["id"]


def test_purchase_invoice_cascade(client):
    headers = login(client)
    cat_id, product_id = _seed_product(client, headers)
    supplier_id = _seed_supplier(client, headers)

    payload = {
        "supplier_id": supplier_id,
        "date": "2026-06-30T00:00:00",
        "items": [{"product_id": product_id, "quantity": 5, "unit_cost": 50000, "tax_pct": 9}],
        "payment_method": "credit",
        "payment_status": "unpaid",
    }
    resp = client.post("/api/v1/purchase-invoices", json=payload, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["number"].startswith("INV-P")
    assert body["data"]["total"] > 0

    inv_id = body["meta"]["id"]
    get_resp = client.get(f"/api/v1/purchase-invoices/{inv_id}", headers=headers)
    assert get_resp.status_code == 200
    assert len(get_resp.json()["data"]["items"]) == 1


def test_sale_invoice_cascade(client):
    headers = login(client)
    cat_id, product_id = _seed_product(client, headers)
    customer_id = _seed_customer(client, headers)
    supplier_id = _seed_supplier(client, headers)

    # Physical products must have stock before a sale can post.
    purchase_payload = {
        "supplier_id": supplier_id,
        "date": "2026-06-29T00:00:00",
        "items": [{"product_id": product_id, "quantity": 5, "unit_cost": 50000}],
        "payment_method": "credit",
        "payment_status": "unpaid",
    }
    purchase_resp = client.post("/api/v1/purchase-invoices", json=purchase_payload, headers=headers)
    assert purchase_resp.status_code == 200

    payload = {
        "customer_id": customer_id,
        "date": "2026-06-30T00:00:00",
        "items": [{"product_id": product_id, "quantity": 2, "unit_price": 100000, "tax_pct": 9}],
        "payment_method": "cash",
        "payment_status": "paid",
    }
    resp = client.post("/api/v1/sale-invoices", json=payload, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["number"].startswith("INV-S")

    inv_id = body["meta"]["id"]
    get_resp = client.get(f"/api/v1/sale-invoices/{inv_id}", headers=headers)
    assert get_resp.status_code == 200
    assert len(get_resp.json()["data"]["items"]) == 1
