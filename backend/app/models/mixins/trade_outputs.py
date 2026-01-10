# app/models/mixins/trade_outputs.py

from sqlalchemy.orm import Mapped, mapped_column

class TradeOutputMixin:
    sl_price: Mapped[float]
    tp_price: Mapped[float]
    risk_distance_price: Mapped[float | None]
    reward_distance_price: Mapped[float | None]
    value_per_unit_1lot_chf: Mapped[float | None]
    stop_value_1lot_chf: Mapped[float | None]
    exposure_units: Mapped[float | None]
