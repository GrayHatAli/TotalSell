def test_admin_can_login_and_read_profile(client):
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "ChangeMe123!"},
    )

    assert login_response.status_code == 200
    token_data = login_response.json()["data"]
    assert token_data["access_token"]
    assert token_data["refresh_token"]

    profile_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    )

    assert profile_response.status_code == 200
    profile = profile_response.json()["data"]
    assert profile["email"] == "admin@example.com"
    assert profile["is_admin"] is True


def test_invalid_login_uses_error_envelope(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "http_error"

