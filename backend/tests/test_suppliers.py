import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def test_supplier_crud(client):
    headers = login(client)

    create_resp = client.post("/api/v1/suppliers", json={"name": "Tehran Electronics", "phone": "02112345678", "tax_id": "TAX-123"}, headers=headers)
    assert create_resp.status_code == 200
    body = create_resp.json()
    assert body["success"] is True
    supplier_id = body["meta"]["id"]

    get_resp = client.get(f"/api/v1/suppliers/{supplier_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["tax_id"] == "TAX-123"

    update_resp = client.patch(f"/api/v1/suppliers/{supplier_id}", json={"payment_terms": "Net 30"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["payment_terms"] == "Net 30"

    delete_resp = client.delete(f"/api/v1/suppliers/{supplier_id}", headers=headers)
    assert delete_resp.status_code == 200

    get_after = client.get(f"/api/v1/suppliers/{supplier_id}", headers=headers)
    assert get_after.status_code == 404


def test_supplier_list_search(client):
    headers = login(client)
    client.post("/api/v1/suppliers", json={"name": "Tehran Electronics", "phone": "02112345678"}, headers=headers)
    client.post("/api/v1/suppliers", json={"name": "Mashhad Parts", "phone": "05112345678"}, headers=headers)

    resp = client.get("/api/v1/suppliers?search=Tehran", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] == 1
