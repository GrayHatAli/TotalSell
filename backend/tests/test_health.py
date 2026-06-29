def test_health_endpoint_returns_envelope(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"] == {"status": "ok"}
    assert body["error"] is None


def test_database_health_endpoint_returns_envelope(client):
    response = client.get("/api/v1/health/db")

    assert response.status_code == 200
    assert response.json()["data"] == {"status": "ok"}

