# app/models/trade.py

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins.timestamps import TimestampMixin
from app.models.mixins.trade_inputs import TradeInputMixin
from app.models.mixins.trade_outputs import TradeOutputMixin


class Trade(
    Base,
    TimestampMixin,
    TradeInputMixin,
    TradeOutputMixin,
):
    __tablename__ = "trades"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    symbol: Mapped[str]
    direction: Mapped[str]
    lots: Mapped[float]
    risk_chf: Mapped[float]
    reward_chf: Mapped[float]

    status: Mapped[str]
    note: Mapped[str | None]

    user = relationship("User", back_populates="trades")
