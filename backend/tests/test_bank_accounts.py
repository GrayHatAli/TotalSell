import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def test_bank_account_crud(client):
    headers = login(client)
    create = client.post("/api/v1/bank-accounts", json={"name": "Main Bank", "account_type": "bank", "opening_balance": 1000000}, headers=headers)
    assert create.status_code == 200
    acc_id = create.json()["meta"]["id"]

    get_resp = client.get(f"/api/v1/bank-accounts/{acc_id}", headers=headers)
    assert get_resp.status_code == 200

    update = client.patch(f"/api/v1/bank-accounts/{acc_id}", json={"bank_name": "Test Bank"}, headers=headers)
    assert update.status_code == 200
    assert update.json()["data"]["bank_name"] == "Test Bank"

    delete_resp = client.delete(f"/api/v1/bank-accounts/{acc_id}", headers=headers)
    assert delete_resp.status_code == 200

    get_after = client.get(f"/api/v1/bank-accounts/{acc_id}", headers=headers)
    assert get_after.status_code == 404
