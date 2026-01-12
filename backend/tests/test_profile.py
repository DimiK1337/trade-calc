# tests/test_profile.py

from fastapi.testclient import TestClient

from tests.utils.auth import register_user, get_token, auth_headers, login_user_raw, login_user


def test_profile_get_requires_auth(client: TestClient):
    r = client.get("/api/v1/profile")
    assert r.status_code == 401, r.text


def test_profile_get_returns_user(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")

    token = get_token(client, "a@example.com", "test1234")
    me = client.get("/api/v1/profile", headers=auth_headers(token))
    assert me.status_code == 200, me.text
    body = me.json()
    assert body["email"] == "a@example.com"
    assert body["username"] == "alice"


def test_profile_patch_username_success(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = get_token(client, "a@example.com", "test1234")

    r = client.patch(
        "/api/v1/profile",
        json={"username": "alice2"},
        headers=auth_headers(token),
    )
    assert r.status_code == 200, r.text
    assert r.json()["username"] == "alice2"

    # login should work with new username too
    token2 = get_token(client, "alice2", "test1234")
    assert isinstance(token2, str) and len(token2) > 10


def test_profile_patch_username_duplicate_fails(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    register_user(client, "b@example.com", "bob", "test1234")

    token = get_token(client, "a@example.com", "test1234")
    r = client.patch(
        "/api/v1/profile",
        json={"username": "bob"},
        headers=auth_headers(token),
    )
    assert r.status_code == 400, r.text


def test_profile_patch_email_requires_password(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = get_token(client, "a@example.com", "test1234")

    r = client.patch(
        "/api/v1/profile",
        json={"email": "new@example.com"},
        headers=auth_headers(token),
    )
    assert r.status_code == 400, r.text


def test_profile_patch_email_success_with_password(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = get_token(client, "a@example.com", "test1234")

    r = client.patch(
        "/api/v1/profile",
        json={"email": "new@example.com", "current_password": "test1234"},
        headers=auth_headers(token),
    )
    assert r.status_code == 200, r.text
    assert r.json()["email"] == "new@example.com"

    # login should work with new email
    token2 = get_token(client, "new@example.com", "test1234")
    assert isinstance(token2, str) and len(token2) > 10


def test_profile_change_password_success(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = get_token(client, "a@example.com", "test1234")

    r = client.post(
        "/api/v1/profile/password",
        json={"current_password": "test1234", "new_password": "newpass123"},
        headers=auth_headers(token),
    )
    assert r.status_code == 204, r.text

    # old password fails
    bad = login_user_raw(client, "a@example.com", "test1234")
    assert bad.status_code == 401, bad.text

    # new password works
    token2 = get_token(client, "a@example.com", "newpass123")
    assert isinstance(token2, str) and len(token2) > 10


def test_profile_delete_account(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = get_token(client, "a@example.com", "test1234")

    r = client.request(
        "DELETE",
        "/api/v1/profile",
        json={"current_password": "test1234"},
        headers=auth_headers(token),
    )
    assert r.status_code == 204, r.text

    # login should fail now
    bad = login_user_raw(client, "a@example.com", "test1234")
    assert bad.status_code == 401, bad.text
