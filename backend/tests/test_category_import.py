import io
import os

from openpyxl import Workbook


def login(client):
    resp = client.post("/api/v1/auth/login", json={"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def make_xlsx(rows):
    wb = Workbook()
    ws = wb.active
    assert ws is not None
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def test_import_creates_categories_with_codes(client):
    headers = login(client)
    xlsx = make_xlsx([
        ["name", "slug", "parent", "active"],
        ["Beverages", "beverages", "", "yes"],
        ["Dairy", "dairy", "Beverages", "1"],
    ])
    resp = client.post(
        "/api/v1/categories/import",
        files={"file": ("cats.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["created"] == 2
    assert body["data"]["failed"] == 0

    listed = client.get("/api/v1/categories", headers=headers).json()["data"]
    by_name = {c["name"]: c for c in listed}
    assert by_name["Beverages"]["code"] == "1000"
    assert by_name["Dairy"]["code"] == "1100"
    assert by_name["Dairy"]["parent_id"] == by_name["Beverages"]["id"]


def test_import_rejects_missing_name_column(client):
    headers = login(client)
    xlsx = make_xlsx([["title"], ["oops"]])
    resp = client.post(
        "/api/v1/categories/import",
        files={"file": ("cats.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=headers,
    )
    assert resp.status_code == 400


def test_import_skips_duplicate_slugs(client):
    headers = login(client)
    client.post("/api/v1/categories", json={"name": "Existing", "slug": "existing"}, headers=headers)
    xlsx = make_xlsx([
        ["name", "slug"],
        ["Other", "existing"],
        ["Fresh", "fresh"],
    ])
    resp = client.post(
        "/api/v1/categories/import",
        files={"file": ("cats.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["data"]["created"] == 1
    assert body["data"]["skipped"] == 1