from __future__ import annotations

from fastapi.testclient import TestClient


def register_user(client: TestClient, email: str, username: str, password: str) -> dict:
    r = client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": password},
    )
    assert r.status_code in (200, 201), r.text
    return r.json()


def login_user_raw(client: TestClient, identifier: str, password: str):
    """
    Returns the raw response. Use this in tests where login is expected to fail.
    """
    return client.post(
        "/api/v1/auth/token",
        data={"username": identifier, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def login_user(client: TestClient, identifier: str, password: str) -> str:
    """
    Returns an access token string. Use this in tests where login is expected to succeed.
    """
    r = login_user_raw(client, identifier=identifier, password=password)
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def get_token(client: TestClient, identifier: str, password: str) -> str:
    # Alias for readability
    return login_user(client, identifier=identifier, password=password)


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
