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


def test_barcode_lookup_online_local_hit(client, monkeypatch):
    headers = login(client)
    cat = client.post("/api/v1/categories", json={"name": "Cat"}, headers=headers).json()["meta"]["id"]
    client.post("/api/v1/products", json={"name": "P3", "barcode": "BAR-789", "category_id": cat, "sale_price": 100, "cost_price": 60}, headers=headers)

    # Must NOT hit the network when the product exists locally.
    monkeypatch.setattr("app.routers.products.lookup_barcode_online", lambda code: (_ for _ in ()).throw(AssertionError("network should not be called")))

    resp = client.get("/api/v1/products/barcode-lookup-online?code=BAR-789", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["found"] is True
    assert body["data"]["local"] is True
    assert body["data"]["product"]["name"] == "P3"


def test_barcode_lookup_online_found_externally(client, monkeypatch):
    headers = login(client)
    monkeypatch.setattr(
        "app.routers.products.lookup_barcode_online",
        lambda code: {
            "name": "Coca-Cola",
            "brand": "Coca-Cola",
            "image_url": "https://example.com/img.jpg",
            "quantity": "330 ml",
            "category": "Beverages",
            "source": "openfoodfacts",
        },
    )
    resp = client.get("/api/v1/products/barcode-lookup-online?code=5449000000996", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["data"]["found"] is True
    assert body["data"]["local"] is False
    assert body["data"]["product"]["name"] == "Coca-Cola"
    assert body["data"]["product"]["source"] == "openfoodfacts"


def test_barcode_lookup_online_not_found(client, monkeypatch):
    headers = login(client)
    monkeypatch.setattr("app.routers.products.lookup_barcode_online", lambda code: None)
    resp = client.get("/api/v1/products/barcode-lookup-online?code=9999999999999", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["found"] is False
    assert body["data"]["product"] is None
