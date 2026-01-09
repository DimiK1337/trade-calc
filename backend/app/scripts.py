from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _main_path() -> str:
    # Works from anywhere; points to app/main.py
    here = Path(__file__).resolve()
    return str(here.parent / "main.py")


def dev() -> None:
    """
    Development server:
    - auto-reload
    - nice logs
    """
    cmd = ["fastapi", "dev", _main_path()]
    raise SystemExit(subprocess.call(cmd))


def prod() -> None:
    """
    Production-ish server:
    - no reload
    - host/port configurable via env vars
    """
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "8000")

    cmd = [
        "fastapi",
        "run",
        _main_path(),
        "--host",
        host,
        "--port",
        str(port),
    ]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    mode = (sys.argv[1] if len(sys.argv) > 1 else "dev").lower()
    prod() if mode == "prod" else dev()
