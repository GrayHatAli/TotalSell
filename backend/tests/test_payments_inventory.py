import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def _seed_stock(client, headers, product_id, supplier_id, quantity=5):
    purchase_payload = {
        "supplier_id": supplier_id,
        "date": "2026-06-29T00:00:00",
        "items": [{"product_id": product_id, "quantity": quantity, "unit_cost": 50000}],
        "payment_method": "credit",
        "payment_status": "unpaid",
    }
    resp = client.post("/api/v1/purchase-invoices", json=purchase_payload, headers=headers)
    assert resp.status_code == 200


def test_payment_crud(client):
    headers = login(client)
    cat_id, product_id = _seed_product(client, headers)
    customer_id = _seed_customer(client, headers)
    supplier_id = _seed_supplier(client, headers)
    _seed_stock(client, headers, product_id, supplier_id)

    sale_payload = {
        "customer_id": customer_id,
        "date": "2026-06-30T00:00:00",
        "items": [{"product_id": product_id, "quantity": 1, "unit_price": 100000}],
        "payment_method": "credit",
        "payment_status": "unpaid",
    }
    sale_resp = client.post("/api/v1/sale-invoices", json=sale_payload, headers=headers)
    inv_id = sale_resp.json()["meta"]["id"]

    payment_payload = {
        "reference_type": "SALE",
        "reference_id": inv_id,
        "amount": 50000,
        "method": "cash",
        "date": "2026-06-30T00:00:00",
    }
    pay_resp = client.post("/api/v1/payments", json=payment_payload, headers=headers)
    assert pay_resp.status_code == 200
    assert pay_resp.json()["data"]["amount"] == 50000


def test_inventory_movements_list(client):
    headers = login(client)
    cat_id, product_id = _seed_product(client, headers)
    customer_id = _seed_customer(client, headers)
    supplier_id = _seed_supplier(client, headers)
    _seed_stock(client, headers, product_id, supplier_id)

    sale_payload = {
        "customer_id": customer_id,
        "date": "2026-06-30T00:00:00",
        "items": [{"product_id": product_id, "quantity": 1, "unit_price": 100000}],
        "payment_method": "cash",
        "payment_status": "paid",
    }
    client.post("/api/v1/sale-invoices", json=sale_payload, headers=headers)

    mov_resp = client.get(f"/api/v1/inventory-movements?product_id={product_id}", headers=headers)
    assert mov_resp.status_code == 200
    assert mov_resp.json()["meta"]["total"] >= 1


def _seed_supplier(client, headers):
    return client.post("/api/v1/suppliers", json={"name": "Sup"}, headers=headers).json()["meta"]["id"]


def _seed_product(client, headers):
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    return cat, client.post("/api/v1/products", json={"name": "P1", "category_id": cat, "sale_price": 100, "cost_price": 60}, headers=headers).json()["meta"]["id"]


def _seed_customer(client, headers):
    return client.post("/api/v1/customers", json={"name": "Cust"}, headers=headers).json()["meta"]["id"]
