# app/models/mixins/trade_inputs.py

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class TradeInputMixin:
    balance_chf: Mapped[float | None] = mapped_column(nullable=True)
    risk_pct: Mapped[float | None] = mapped_column(nullable=True)

    stop_distance: Mapped[float] = mapped_column(nullable=False)
    stop_unit: Mapped[str] = mapped_column(String(8), nullable=False)  # "TICKS" | "PIPS"

    tp_r_multiple: Mapped[float | None] = mapped_column(nullable=True)
    lot_step: Mapped[float | None] = mapped_column(nullable=True)

    usdchf_rate: Mapped[float | None] = mapped_column(nullable=True)
    tick_size: Mapped[float | None] = mapped_column(nullable=True)
    contract_size: Mapped[float | None] = mapped_column(nullable=True)

