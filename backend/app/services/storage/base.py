# app/services/storage/base.py

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, ConfigDict


class StoredImage(BaseModel):
    model_config = ConfigDict(frozen=True)

    trade_id: str
    kind: str
    mime: str
    sha256: str
    byte_size: int


class StoredImageData(StoredImage):
    model_config = ConfigDict(frozen=True)

    data: bytes


class TradeImageStore(Protocol):
    """
    This class exists in order to future proof the project, so that chart images can be stored in an Online Storage Solution (e.g S3)
    """
    def save(self, *, trade_id: str, kind: str, data: bytes, mime: str) -> StoredImage:
        ...

    def get(self, *, trade_id: str, kind: str) -> StoredImageData | None:
        ...

    def delete(self, *, trade_id: str, kind: str) -> None:
        ...
