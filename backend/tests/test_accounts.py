import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def test_accounts_list(client):
    headers = login(client)
    resp = client.get("/api/v1/accounts", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    codes = {a["code"] for a in data}
    expected = {"1110", "1120", "1130", "1140", "1150", "2110", "2120", "4100", "5100"}
    assert expected.issubset(codes)
