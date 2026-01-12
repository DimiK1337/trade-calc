# app/services/storage/db_store.py

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trade_image import TradeImage
from app.services.storage.base import StoredImage, StoredImageData, TradeImageStore
from app.services.storage.image_processing import sha256_hex


class DbTradeImageStore(TradeImageStore):
    def __init__(self, db: Session):
        self.db = db

    def save(self, *, trade_id: str, kind: str, data: bytes, mime: str) -> StoredImage:
        sha = sha256_hex(data)

        row = self.db.scalars(
            select(TradeImage).where(TradeImage.trade_id == trade_id, TradeImage.kind == kind)
        ).first()

        # If identical image already stored, be idempotent
        if row and row.sha256 == sha:
            return StoredImage(
                trade_id=trade_id,
                kind=kind,
                mime=row.mime,
                sha256=row.sha256,
                byte_size=row.byte_size,
            )

        if row:
            row.data = data
            row.mime = mime
            row.sha256 = sha
            row.byte_size = len(data)
            self.db.add(row)
            self.db.commit()
            self.db.refresh(row)
            return StoredImage(
                trade_id=trade_id,
                kind=kind,
                mime=row.mime,
                sha256=row.sha256,
                byte_size=row.byte_size,
            )

        row = TradeImage(
            trade_id=trade_id,
            kind=kind,
            mime=mime,
            sha256=sha,
            byte_size=len(data),
            data=data,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return StoredImage(
            trade_id=trade_id,
            kind=kind,
            mime=row.mime,
            sha256=row.sha256,
            byte_size=row.byte_size,
        )

    def get(self, *, trade_id: str, kind: str) -> StoredImageData | None:
        row = self.db.scalars(
            select(TradeImage).where(TradeImage.trade_id == trade_id, TradeImage.kind == kind)
        ).first()
        if not row:
            return None
        return StoredImageData(
            trade_id=trade_id,
            kind=kind,
            mime=row.mime,
            sha256=row.sha256,
            byte_size=row.byte_size,
            data=row.data,
        )

    def delete(self, *, trade_id: str, kind: str) -> None:
        row = self.db.scalars(
            select(TradeImage).where(TradeImage.trade_id == trade_id, TradeImage.kind == kind)
        ).first()
        if not row:
            return
        self.db.delete(row)
        self.db.commit()
