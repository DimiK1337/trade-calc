# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import router as v1_router

from app.db.init_db import bootstrap_root_admin, ensure_admin_exists
from app.db.migrations_check import ensure_db_is_at_head


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup (fail fast) ---
    ensure_db_is_at_head()

    if settings.BOOTSTRAP_ROOT_ADMIN:
        bootstrap_root_admin()

    if settings.REQUIRE_ADMIN_ON_STARTUP:
        ensure_admin_exists()

    yield

    # --- Shutdown (optional cleanup) ---
    # nothing needed for now

app = FastAPI(title="Trade Calc API", lifespan=lifespan)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/")
def index_page():
    return {"status": "ok", "msg": "go explore other pages"}

@app.get("/health")
def health():
    return {"status": "ok"}
