# tests/test_trades.py

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.utils.auth import auth_headers, login_user, register_user
from tests.utils.trades import create_trade


def test_trades_create_requires_auth(client: TestClient):
    payload = {
        "inputs": {
            "symbol": "XAUUSD",
            "direction": "SHORT",
            "entry_price": 4600.5,
            "stop_distance": 20.0,
            "stop_unit": "TICKS",
        },
        "outputs": {
            "sl_price": 4601.0,
            "tp_price": 4599.5,
            "lots": 0.01,
            "risk_chf": 10.0,
            "reward_chf": 20.0,
            "reward_to_risk": 2.0,
        },
        "journal": {"status": "PLANNED"},
    }
    r = client.post("/api/v1/trades", json=payload)
    assert r.status_code == 401, r.text


def test_trades_create_and_get_and_list(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = login_user(client, "a@example.com", "test1234")

    created = create_trade(client, token)
    trade_id = created["id"]

    # list (newest first)
    lst = client.get("/api/v1/trades", headers=auth_headers(token))
    assert lst.status_code == 200, lst.text
    items = lst.json()
    assert len(items) >= 1
    assert items[0]["id"] == trade_id

    # get detail
    got = client.get(f"/api/v1/trades/{trade_id}", headers=auth_headers(token))
    assert got.status_code == 200, got.text
    body = got.json()
    assert body["id"] == trade_id
    assert body["inputs"]["symbol"] == "XAUUSD"
    assert body["journal"]["status"] == "PLANNED"


def test_trades_forbidden_for_other_user(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    register_user(client, "b@example.com", "bob", "test1234")
    token_a = login_user(client, "a@example.com", "test1234")
    token_b = login_user(client, "b@example.com", "test1234")

    created = create_trade(client, token_a)
    trade_id = created["id"]

    # other user cannot read
    got = client.get(f"/api/v1/trades/{trade_id}", headers=auth_headers(token_b))
    assert got.status_code in (403, 404), got.text

    # other user cannot patch
    patch = client.patch(
        f"/api/v1/trades/{trade_id}",
        json={"status": "CANCELLED"},
        headers=auth_headers(token_b),
    )
    assert patch.status_code in (403, 404), patch.text


def test_trades_patch_limited_fields(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = login_user(client, "a@example.com", "test1234")

    created = create_trade(client, token)
    trade_id = created["id"]

    patch = client.patch(
        f"/api/v1/trades/{trade_id}",
        json={"status": "OPEN", "note": "entered"},
        headers=auth_headers(token),
    )
    assert patch.status_code == 200, patch.text
    body = patch.json()
    assert body["journal"]["status"] == "OPEN"
    assert body["journal"]["note"] == "entered"

    # ensure forbidden field update gets rejected (extra="forbid")
    bad = client.patch(
        f"/api/v1/trades/{trade_id}",
        json={"symbol": "EURUSD"},
        headers=auth_headers(token),
    )
    assert bad.status_code == 422, bad.text
