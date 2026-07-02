import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def test_barcode_lookup_by_sku(client):
    headers = login(client)
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    client.post("/api/v1/products", json={"name": "P1", "sku": "SKU-123", "category_id": cat, "sale_price": 100, "cost_price": 60}, headers=headers)
    resp = client.get("/api/v1/products/barcode-lookup?code=SKU-123", headers=headers)
    print("STATUS:", resp.status_code, "BODY:", resp.text[:500])
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["name"] == "P1"


def test_barcode_lookup_by_barcode(client):
    headers = login(client)
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    client.post("/api/v1/products", json={"name": "P2", "barcode": "BAR-456", "category_id": cat, "sale_price": 200, "cost_price": 120}, headers=headers)
    resp = client.get("/api/v1/products/barcode-lookup?code=BAR-456", headers=headers)
    print("STATUS:", resp.status_code, "BODY:", resp.text[:500])
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["name"] == "P2"


def test_barcode_lookup_not_found(client):
    headers = login(client)
    resp = client.get("/api/v1/products/barcode-lookup?code=UNKNOWN", headers=headers)
    print("STATUS:", resp.status_code, "BODY:", resp.text[:500])
    assert resp.status_code == 404
