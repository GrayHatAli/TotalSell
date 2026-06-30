import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def test_product_crud(client):
    headers = login(client)
    cat_resp = client.post("/api/v1/categories", json={"name": "Electronics"}, headers=headers)
    category_id = cat_resp.json()["meta"]["id"]

    tag_resp = client.post("/api/v1/tags", json={"name": "new"}, headers=headers)
    tag_id = tag_resp.json()["meta"]["id"]

    payload = {
        "name": "Test Product",
        "sku": "TP-001",
        "barcode": "123456789",
        "category_id": category_id,
        "sale_price": 100000,
        "cost_price": 60000,
        "product_type": "physical",
        "tag_ids": [tag_id],
        "custom_attributes": {"material": "plastic", "warranty_months": 12},
    }

    create_resp = client.post("/api/v1/products", json=payload, headers=headers)
    assert create_resp.status_code == 200
    body = create_resp.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Test Product"
    product_id = body["meta"]["id"]

    get_resp = client.get(f"/api/v1/products/{product_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["custom_attributes"]["warranty_months"] == 12

    update_resp = client.patch(f"/api/v1/products/{product_id}", json={"sale_price": 120000}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["sale_price"] == 120000

    delete_resp = client.delete(f"/api/v1/products/{product_id}", headers=headers)
    assert delete_resp.status_code == 200

    get_after = client.get(f"/api/v1/products/{product_id}", headers=headers)
    assert get_after.status_code == 404


def test_product_list_filtering(client):
    headers = login(client)
    cat_resp = client.post("/api/v1/categories", json={"name": "Cat1"}, headers=headers)
    cat_id = cat_resp.json()["meta"]["id"]

    client.post("/api/v1/products", json={"name": "Prod A", "category_id": cat_id, "product_type": "physical"}, headers=headers)
    client.post("/api/v1/products", json={"name": "Prod B", "category_id": cat_id, "product_type": "service"}, headers=headers)

    resp = client.get(f"/api/v1/products?category_id={cat_id}&product_type=service", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] == 1
