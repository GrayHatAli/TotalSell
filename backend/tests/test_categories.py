import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def test_category_crud(client):
    headers = login(client)

    create_resp = client.post("/api/v1/categories", json={"name": "Electronics"}, headers=headers)
    assert create_resp.status_code == 200
    cat_id = create_resp.json()["meta"]["id"]

    get_resp = client.get(f"/api/v1/categories/{cat_id}", headers=headers)
    assert get_resp.status_code == 200

    update_resp = client.patch(f"/api/v1/categories/{cat_id}", json={"slug": "electronics"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["slug"] == "electronics"

    delete_resp = client.delete(f"/api/v1/categories/{cat_id}", headers=headers)
    assert delete_resp.status_code == 200

    get_after = client.get(f"/api/v1/categories/{cat_id}", headers=headers)
    assert get_after.status_code == 404


def test_category_parent_validation(client):
    headers = login(client)
    parent_resp = client.post("/api/v1/categories", json={"name": "Root"}, headers=headers)
    parent_id = parent_resp.json()["meta"]["id"]

    child_resp = client.post("/api/v1/categories", json={"name": "Child", "parent_id": parent_id}, headers=headers)
    assert child_resp.status_code == 200

    bad_resp = client.post("/api/v1/categories", json={"name": "Orphan", "parent_id": 99999}, headers=headers)
    assert bad_resp.status_code == 400
    assert bad_resp.json()["error"]["code"] == "http_error"


def test_category_slug_unique(client):
    headers = login(client)
    client.post("/api/v1/categories", json={"name": "A", "slug": "unique-slug"}, headers=headers)
    dup = client.post("/api/v1/categories", json={"name": "B", "slug": "unique-slug"}, headers=headers)
    assert dup.status_code == 400
