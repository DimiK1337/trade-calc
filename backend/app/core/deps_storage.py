# app/core/deps_storage.py

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.services.storage.base import TradeImageStore
from app.services.storage.db_store import DbTradeImageStore


def get_trade_image_store(db: Session = Depends(get_db)) -> TradeImageStore:
    # Later: return S3TradeImageStore(...) here
    return DbTradeImageStore(db)
