# tests/test_auth.py

from fastapi.testclient import TestClient

def register_user(client: TestClient, email: str, username: str, password: str):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "username": username},
    )


def login_user(
    client: TestClient,
    *,
    password: str,
    email: str | None = None,
    username: str | None = None,
):
    """
    OAuth2PasswordRequestForm uses a field named "username" for the identifier.
    We treat that identifier as either email or username.

    Rules:
    - If neither email nor username provided -> ValueError
    - If both provided -> email wins
    """
    identifier = email or username
    if not identifier:
        raise ValueError("Provide either email or username (non-empty).")

    return client.post(
        "/api/v1/auth/token",
        data={"username": identifier, "password": password},
    )


def test_register_success(client: TestClient):
    r = register_user(client, "dimi@example.com", "dimi", "test1234")
    assert r.status_code == 200, r.text
    body = r.json()

    assert "id" in body
    assert body["email"] == "dimi@example.com"
    assert body["username"] == "dimi"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email_fails(client: TestClient):
    r1 = register_user(client, "dimi@example.com", "dimi", "test1234")
    assert r1.status_code == 200, r1.text

    r2 = register_user(client, "dimi@example.com", "dimi2", "test1234")
    assert r2.status_code in (400, 409), r2.text


def test_login_with_email_success_returns_token(client: TestClient):
    reg = register_user(client, "dimi@example.com", "dimi", "test1234")
    assert reg.status_code == 200, reg.text

    login = login_user(client, email="dimi@example.com", password="test1234")
    assert login.status_code == 200, login.text
    body = login.json()

    assert "access_token" in body
    assert body.get("token_type") == "bearer"


def test_login_with_username_success_returns_token(client: TestClient):
    reg = register_user(client, "dimi@example.com", "dimi", "test1234")
    assert reg.status_code == 200, reg.text

    login = login_user(client, username="dimi", password="test1234")
    print(f"STDOUT {login = }")
    assert login.status_code == 200, login.text
    body = login.json()

    assert "access_token" in body
    assert body.get("token_type") == "bearer"


def test_login_wrong_password_fails(client: TestClient):
    reg = register_user(client, "dimi@example.com", "dimi", "test1234")
    assert reg.status_code == 200, reg.text

    login = login_user(client, email="dimi@example.com", password="wrong-password")
    assert login.status_code == 401, login.text


def test_me_requires_auth(client: TestClient):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401, r.text


def test_me_with_token_returns_user(client: TestClient):
    reg = register_user(client, "dimi@example.com", "dimi", "test1234")
    assert reg.status_code == 200, reg.text

    login = login_user(client, email="dimi@example.com", password="test1234")
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200, me.text
    body = me.json()

    assert body["email"] == "dimi@example.com"
    assert body["username"] == "dimi"
    assert "id" in body
