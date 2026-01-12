# tests/utils/trades.py

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from app.schemas.trade import TradeCreate, TradeDirection, TradeStatus, StopUnit
from tests.utils.auth import auth_headers


def make_trade_payload(**overrides: Any) -> dict[str, Any]:
    """
    Build a valid TradeCreate payload and validate it locally
    so tests fail with a clear Pydantic error if the schema changes.
    """
    payload: dict[str, Any] = {
        "inputs": {
            "balance_chf": 1000.0,
            "risk_pct": 1.0,
            "symbol": "XAUUSD",
            "direction": TradeDirection.SHORT,
            "entry_price": 4600.5,
            "stop_distance": 20.0,
            "stop_unit": StopUnit.TICKS,
            "tp_r_multiple": 2.0,
            "lot_step": 0.01,
            "usdchf_rate": 0.90,
            "tick_size": 0.01,
            "contract_size": 100.0,
        },
        "outputs": {
            "sl_price": 4601.0,
            "tp_price": 4599.5,
            "risk_distance_price": 0.5,
            "reward_distance_price": 1.0,
            "lots": 0.01,
            "risk_chf": 10.0,
            "reward_chf": 20.0,
            "reward_to_risk": 2.0,
            "value_per_unit_1lot_chf": 0.9,
            "stop_value_1lot_chf": 9.0,
            "exposure_units": 1.0,
        },
        "journal": {
            "note": "planned trade",
            "status": TradeStatus.PLANNED,
            "opened_at": None,
            "closed_at": None,
            "realized_pnl_chf": None,
            "realized_r_multiple": None,
        },
    }

    # Allow targeted overrides at any depth:
    # Example: make_trade_payload(journal={"status": "OPEN"})
    for k, v in overrides.items():
        if isinstance(v, dict) and isinstance(payload.get(k), dict):
            payload[k].update(v)  # type: ignore[union-attr]
        else:
            payload[k] = v

    # Local validation (raises a clear error if schema mismatches)
    TradeCreate.model_validate(payload)
    return payload


def create_trade(client: TestClient, token: str, **overrides: Any) -> dict[str, Any]:
    payload = make_trade_payload(**overrides)
    r = client.post("/api/v1/trades", json=payload, headers=auth_headers(token))
    assert r.status_code in (200, 201), r.text
    return r.json()
