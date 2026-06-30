import os


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def test_tag_crud(client):
    headers = login(client)

    create_resp = client.post("/api/v1/tags", json={"name": "bestseller", "color": "#ff0000"}, headers=headers)
    assert create_resp.status_code == 200
    tag_id = create_resp.json()["meta"]["id"]

    list_resp = client.get("/api/v1/tags", headers=headers)
    assert list_resp.status_code == 200
    assert any(t["id"] == tag_id for t in list_resp.json()["data"])

    dup_resp = client.post("/api/v1/tags", json={"name": "bestseller"}, headers=headers)
    assert dup_resp.status_code == 400
