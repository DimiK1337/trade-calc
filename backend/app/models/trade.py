# app/models/trade.py

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
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

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # Core trade identity
    symbol: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)  # "LONG" | "SHORT"

    # Planner core input
    entry_price: Mapped[float] = mapped_column(nullable=False)

    # Calculated sizing outputs
    lots: Mapped[float] = mapped_column(nullable=False)
    risk_chf: Mapped[float] = mapped_column(nullable=False)
    reward_chf: Mapped[float] = mapped_column(nullable=False)
    reward_to_risk: Mapped[float] = mapped_column(nullable=False)

    # Journal
    status: Mapped[str] = mapped_column(String(12), nullable=False, server_default="PLANNED")
    note: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    realized_pnl_chf: Mapped[float | None] = mapped_column(nullable=True)
    realized_r_multiple: Mapped[float | None] = mapped_column(nullable=True)

    user = relationship("User", back_populates="trades")
    images = relationship(
        "TradeImage",
        back_populates="trade",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
