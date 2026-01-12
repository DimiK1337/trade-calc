# app/models/trade_images.py

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins.timestamps import TimestampMixin


class TradeImage(Base, TimestampMixin):
    __tablename__ = "trade_images"
    __table_args__ = (
        UniqueConstraint("trade_id", "kind", name="uq_trade_images_trade_kind"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    trade_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("trades.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # For now: only "CHART"
    kind: Mapped[str] = mapped_column(String(16), nullable=False, server_default="CHART")

    mime: Mapped[str] = mapped_column(String(64), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    byte_size: Mapped[int] = mapped_column(nullable=False)

    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    trade = relationship("Trade", back_populates="images")
