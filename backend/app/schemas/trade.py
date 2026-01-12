# app/schemas/trade.py

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StopUnit(str, Enum):
    TICKS = "TICKS"
    PIPS = "PIPS"

class TradeDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class TradeStatus(str, Enum):
    PLANNED = "PLANNED"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class TradeInputs(BaseModel):
    balance_chf: Optional[float] = None
    risk_pct: Optional[float] = None

    symbol: str = Field(min_length=1, max_length=32)
    direction: TradeDirection
    entry_price: float

    stop_distance: float
    stop_unit: StopUnit

    tp_r_multiple: Optional[float] = None
    lot_step: Optional[float] = None

    usdchf_rate: Optional[float] = None
    tick_size: Optional[float] = None
    contract_size: Optional[float] = None

class TradeOutputs(BaseModel):
    sl_price: float
    tp_price: float

    risk_distance_price: Optional[float] = None
    reward_distance_price: Optional[float] = None

    lots: float
    risk_chf: float
    reward_chf: float
    reward_to_risk: float

    value_per_unit_1lot_chf: Optional[float] = None
    stop_value_1lot_chf: Optional[float] = None
    exposure_units: Optional[float] = None

class TradeJournal(BaseModel):
    note: Optional[str] = Field(default=None, max_length=2000)
    status: TradeStatus = TradeStatus.PLANNED

    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    realized_pnl_chf: Optional[float] = None
    realized_r_multiple: Optional[float] = None


class TradeCreate(BaseModel):
    inputs: TradeInputs
    outputs: TradeOutputs
    journal: TradeJournal


class TradeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # limited fields only
    note: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TradeStatus] = None
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    realized_pnl_chf: Optional[float] = None
    realized_r_multiple: Optional[float] = None

class TradeSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime

    symbol: str
    direction: str
    status: str

    outputs: TradeOutputs

class TradeDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    inputs: TradeInputs
    outputs: TradeOutputs
    journal: TradeJournal
