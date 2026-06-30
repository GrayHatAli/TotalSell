import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_customer_crud(client):
    headers = login(client)

    create_resp = client.post("/api/v1/customers", json={"name": "Ali Ahmadi", "phone": "09120000000", "email": "ali@example.com"}, headers=headers)
    assert create_resp.status_code == 200
    body = create_resp.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Ali Ahmadi"
    customer_id = body["meta"]["id"]

    get_resp = client.get(f"/api/v1/customers/{customer_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["phone"] == "09120000000"

    list_resp = client.get("/api/v1/customers?search=Ali", headers=headers)
    assert list_resp.status_code == 200
    assert list_resp.json()["meta"]["total"] == 1

    update_resp = client.patch(f"/api/v1/customers/{customer_id}", json={"credit_limit": 500000}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["credit_limit"] == 500000

    delete_resp = client.delete(f"/api/v1/customers/{customer_id}", headers=headers)
    assert delete_resp.status_code == 200

    get_after = client.get(f"/api/v1/customers/{customer_id}", headers=headers)
    assert get_after.status_code == 404


def test_customer_list_pagination(client):
    headers = login(client)
    for i in range(5):
        client.post("/api/v1/customers", json={"name": f"Customer {i}", "phone": f"0912000000{i}"}, headers=headers)

    resp = client.get("/api/v1/customers?page=2&page_size=2", headers=headers)
    assert resp.status_code == 200
    meta = resp.json()["meta"]
    assert meta["page"] == 2
    assert meta["page_size"] == 2
    assert meta["total"] >= 5
