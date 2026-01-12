# app/services/storage/image_processing.py

from __future__ import annotations

import hashlib
from io import BytesIO

from PIL import Image


class ImageTooLargeError(ValueError):
    pass


class InvalidImageError(ValueError):
    pass


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compress_chart_image(
    raw: bytes,
    *,
    max_upload_bytes: int = 10 * 1024 * 1024,  # 10MB
    max_dim: int = 1600,
    webp_quality: int = 80,
) -> tuple[bytes, str, str]:
    """
    Returns (compressed_bytes, mime, sha256_hex).
    Output is always WebP for consistent storage and small size.
    """
    if len(raw) > max_upload_bytes:
        raise ImageTooLargeError(f"Upload too large (>{max_upload_bytes} bytes)")

    try:
        img = Image.open(BytesIO(raw))
        img.load()
    except Exception as e:
        raise InvalidImageError("Invalid image") from e

    # Normalize mode for WebP
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    img.thumbnail((max_dim, max_dim))

    out = BytesIO()
    img.save(out, format="WEBP", quality=webp_quality, method=6)
    compressed = out.getvalue()

    return compressed, "image/webp", sha256_hex(compressed)
