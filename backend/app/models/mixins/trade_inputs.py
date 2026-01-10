# app/models/mixins/trade_inputs.py

from sqlalchemy.orm import Mapped

class TradeInputMixin:
    balance_chf: Mapped[float | None]
    risk_pct: Mapped[float | None]
    stop_distance: Mapped[float]
    stop_unit: Mapped[str]
    tp_r_multiple: Mapped[float | None]
    lot_step: Mapped[float | None]
