# tests/test_trade_images.py

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from tests.utils.auth import auth_headers, login_user, register_user
from tests.utils.trades import create_trade


ASSETS = Path(__file__).parent / "assets"
CHART_PATH = ASSETS / "MT5_chart.png"


def test_trade_list_has_charts_false_then_true_after_upload(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = login_user(client, "a@example.com", "test1234")

    created = create_trade(client, token)
    trade_id = created["id"]

    lst = client.get("/api/v1/trades", headers=auth_headers(token))
    assert lst.status_code == 200, lst.text
    found = [t for t in lst.json() if t["id"] == trade_id][0]
    assert found["has_charts"] is False

    img_bytes = CHART_PATH.read_bytes()
    up = client.post(
        f"/api/v1/trades/{trade_id}/chart",
        headers=auth_headers(token),
        files={"file": ("mt5_chart.png", img_bytes, "image/png")},
    )
    assert up.status_code == 204, up.text

    lst2 = client.get("/api/v1/trades", headers=auth_headers(token))
    assert lst2.status_code == 200, lst2.text
    found2 = [t for t in lst2.json() if t["id"] == trade_id][0]
    assert found2["has_charts"] is True


def test_trade_chart_get_returns_image(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = login_user(client, "a@example.com", "test1234")

    created = create_trade(client, token)
    trade_id = created["id"]

    img_bytes = CHART_PATH.read_bytes()
    up = client.post(
        f"/api/v1/trades/{trade_id}/chart",
        headers=auth_headers(token),
        files={"file": ("mt5_chart.png", img_bytes, "image/png")},
    )
    assert up.status_code == 204, up.text

    get_img = client.get(f"/api/v1/trades/{trade_id}/chart", headers=auth_headers(token))
    assert get_img.status_code == 200, get_img.text
    assert get_img.headers["content-type"].startswith("image/")
    assert len(get_img.content) > 1000


def test_trade_chart_forbidden_for_other_user(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    register_user(client, "b@example.com", "bob", "test1234")
    token_a = login_user(client, "a@example.com", "test1234")
    token_b = login_user(client, "b@example.com", "test1234")

    created = create_trade(client, token_a)
    trade_id = created["id"]

    img_bytes = CHART_PATH.read_bytes()
    up = client.post(
        f"/api/v1/trades/{trade_id}/chart",
        headers=auth_headers(token_b),
        files={"file": ("mt5_chart.png", img_bytes, "image/png")},
    )
    assert up.status_code in (403, 404), up.text

    get_img = client.get(f"/api/v1/trades/{trade_id}/chart", headers=auth_headers(token_b))
    assert get_img.status_code in (403, 404), get_img.text


def test_trade_chart_rejects_large_upload(client: TestClient):
    register_user(client, "a@example.com", "alice", "test1234")
    token = login_user(client, "a@example.com", "test1234")

    created = create_trade(client, token)
    trade_id = created["id"]

    too_big = b"x" * (10 * 1024 * 1024 + 1)  # 10MB + 1
    up = client.post(
        f"/api/v1/trades/{trade_id}/chart",
        headers=auth_headers(token),
        files={"file": ("big.png", too_big, "image/png")},
    )
    assert up.status_code == 413, up.text
