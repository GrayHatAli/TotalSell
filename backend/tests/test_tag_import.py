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
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def post_import(client, headers, xlsx):
    return client.post(
        "/api/v1/tags/import",
        files={"file": ("tags.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=headers,
    )


def test_import_creates_tags_with_colors(client):
    headers = login(client)
    resp = post_import(client, headers, make_xlsx([
        ["name", "color"],
        ["New", "#ff0000"],
        ["Sale", "green"],
        ["NoColor", ""],
    ]))
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["created"] == 3
    assert body["data"]["skipped"] == 0
    assert body["data"]["failed"] == 0

    tags = {t["name"]: t for t in client.get("/api/v1/tags", headers=headers).json()["data"]}
    assert tags["New"]["color"] == "#ff0000"
    assert tags["Sale"]["color"] == "green"
    assert tags["NoColor"]["color"] is None


def test_import_skips_duplicate_names(client):
    headers = login(client)
    client.post("/api/v1/tags", json={"name": "Existing", "color": "#00ff00"}, headers=headers)
    resp = post_import(client, headers, make_xlsx([
        ["name", "color"],
        ["Existing", "#0000ff"],
        ["Fresh", "#123456"],
    ]))
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["data"]["created"] == 1
    assert body["data"]["skipped"] == 1
    # The existing tag keeps its original color.
    tags = {t["name"]: t for t in client.get("/api/v1/tags", headers=headers).json()["data"]}
    assert tags["Existing"]["color"] == "#00ff00"


def test_import_persian_headers_and_missing_name(client):
    headers = login(client)
    # Persian header names work too.
    resp = post_import(client, headers, make_xlsx([["نام", "رنگ"], ["برچسب۱", "#abcdef"]]))
    assert resp.status_code == 200
    assert resp.json()["data"]["created"] == 1
    # Missing name column -> 400.
    resp = post_import(client, headers, make_xlsx([["title"], ["oops"]]))
    assert resp.status_code == 400


def test_import_counts_failed_rows(client):
    headers = login(client)
    resp = post_import(client, headers, make_xlsx([
        ["name"],
        ["", "ignored"],
        ["x" * 101],
        ["Ok"],
    ]))
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert body["created"] == 1
    assert body["failed"] == 2
    assert [e["row"] for e in body["errors"]] == [2, 3]