import os

import pytest


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def make_tree(client, headers):
    """A(1000) -> d(1100), e(1200) -> f(1210); B(2000) -> c(2100)."""
    ids = {}
    ids["A"] = client.post("/api/v1/categories", json={"name": "A"}, headers=headers).json()["meta"]["id"]
    ids["B"] = client.post("/api/v1/categories", json={"name": "B"}, headers=headers).json()["meta"]["id"]
    ids["d"] = client.post("/api/v1/categories", json={"name": "d", "parent_id": ids["A"]}, headers=headers).json()["meta"]["id"]
    ids["e"] = client.post("/api/v1/categories", json={"name": "e", "parent_id": ids["A"]}, headers=headers).json()["meta"]["id"]
    ids["f"] = client.post("/api/v1/categories", json={"name": "f", "parent_id": ids["e"]}, headers=headers).json()["meta"]["id"]
    ids["c"] = client.post("/api/v1/categories", json={"name": "c", "parent_id": ids["B"]}, headers=headers).json()["meta"]["id"]
    return ids


def get_cat(client, headers, cid):
    return client.get(f"/api/v1/categories/{cid}", headers=headers).json()["data"]


def test_category_codes_hierarchical(client):
    headers = login(client)
    ids = make_tree(client, headers)
    expected = {"A": "1000", "B": "2000", "d": "1100", "e": "1200", "f": "1210", "c": "2100"}
    for key, code in expected.items():
        assert get_cat(client, headers, ids[key])["code"] == code, key


def test_category_manual_code_and_duplicate(client):
    headers = login(client)
    resp = client.post("/api/v1/categories", json={"name": "X", "code": "9000"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["code"] == "9000"
    resp = client.post("/api/v1/categories", json={"name": "Y", "code": "9000"}, headers=headers)
    assert resp.status_code == 400
    # Auto numbering skips manually-taken codes.
    resp = client.post("/api/v1/categories", json={"name": "Z"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["code"] == "1000"


def test_product_sku_auto_generated(client):
    headers = login(client)
    ids = make_tree(client, headers)
    p1 = client.post("/api/v1/products", json={"name": "P1", "category_id": ids["f"], "sale_price": 10}, headers=headers).json()
    assert p1["data"]["sku"] == "1210-0001"
    p2 = client.post("/api/v1/products", json={"name": "P2", "category_id": ids["f"], "sale_price": 10}, headers=headers).json()
    assert p2["data"]["sku"] == "1210-0002"
    # A product in a sibling branch gets its own serial space.
    p3 = client.post("/api/v1/products", json={"name": "P3", "category_id": ids["c"], "sale_price": 10}, headers=headers).json()
    assert p3["data"]["sku"] == "2100-0001"
    # Manual SKU is respected and uniqueness still enforced.
    resp = client.post("/api/v1/products", json={"name": "P4", "sku": "MY-SKU", "category_id": ids["f"]}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["sku"] == "MY-SKU"
    resp = client.post("/api/v1/products", json={"name": "P5", "sku": "MY-SKU", "category_id": ids["f"]}, headers=headers)
    assert resp.status_code == 400
    # No category + no SKU -> SKU stays empty.
    p6 = client.post("/api/v1/products", json={"name": "P6", "sale_price": 1}, headers=headers).json()
    assert p6["data"]["sku"] is None


@pytest.mark.parametrize("payload", [{"name": "P", "category_id": 99999}, {"name": "P"}])
def test_product_create_still_validates(client, payload):
    headers = login(client)
    if "category_id" in payload and payload["category_id"] is not None:
        resp = client.post("/api/v1/products", json=payload, headers=headers)
        assert resp.status_code == 400
    else:
        resp = client.post("/api/v1/products", json=payload, headers=headers)
        assert resp.status_code == 200


def test_delete_category_hard_when_unused(client):
    """No products/subcategories -> row is removed and its code is freed."""
    from app.database import SessionLocal
    from app.models.category import Category as CategoryModel

    headers = login(client)
    cat = client.post("/api/v1/categories", json={"name": "Solo"}, headers=headers).json()["meta"]["id"]
    resp = client.delete(f"/api/v1/categories/{cat}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "deleted_permanently"
    db = SessionLocal()
    try:
        assert db.query(CategoryModel).count() == 0
    finally:
        db.close()
    # The code pool is empty again -> next root starts back at 1000.
    again = client.post("/api/v1/categories", json={"name": "Solo2"}, headers=headers).json()
    assert again["data"]["code"] == "1000"


def test_delete_category_soft_when_has_products(client):
    """Products reference it (even soft-deleted ones) -> soft-delete only."""
    from app.database import SessionLocal
    from app.models.category import Category as CategoryModel

    headers = login(client)
    cat = client.post("/api/v1/categories", json={"name": "Used"}, headers=headers).json()["meta"]["id"]
    client.post("/api/v1/products", json={"name": "P", "category_id": cat}, headers=headers)
    resp = client.delete(f"/api/v1/categories/{cat}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "deleted"
    db = SessionLocal()
    try:
        row = db.get(CategoryModel, cat)
        assert row is not None and row.deleted_at is not None
    finally:
        db.close()


def test_delete_category_soft_when_has_children(client):
    from app.database import SessionLocal
    from app.models.category import Category as CategoryModel

    headers = login(client)
    parent = client.post("/api/v1/categories", json={"name": "Parent"}, headers=headers).json()["meta"]["id"]
    client.post("/api/v1/categories", json={"name": "Child", "parent_id": parent}, headers=headers)
    resp = client.delete(f"/api/v1/categories/{parent}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "deleted"
    # Soft-deleted: row still exists (children reference it) but hidden.
    db = SessionLocal()
    try:
        row = db.get(CategoryModel, parent)
        assert row is not None and row.deleted_at is not None
    finally:
        db.close()