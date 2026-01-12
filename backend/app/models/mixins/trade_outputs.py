# app/models/mixins/trade_outputs.py

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

class TradeOutputMixin:
    sl_price: Mapped[float] = mapped_column(nullable=False)
    tp_price: Mapped[float] = mapped_column(nullable=False)

    risk_distance_price: Mapped[float | None] = mapped_column(nullable=True)
    reward_distance_price: Mapped[float | None] = mapped_column(nullable=True)

    value_per_unit_1lot_chf: Mapped[float | None] = mapped_column(nullable=True)
    stop_value_1lot_chf: Mapped[float | None] = mapped_column(nullable=True)

    # oz for gold; can be None for FX
    exposure_units: Mapped[float | None] = mapped_column(nullable=True)
