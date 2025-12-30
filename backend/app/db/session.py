from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# SQLite needs this in multithreaded apps (FastAPI dev server)
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
  settings.DATABASE_URL, 
  connect_args=connect_args, 
  future=True
)

SessionLocal = sessionmaker(
  bind=engine, 
  autoflush=False, # “Flush” means: send pending changes to the DB (INSERT/UPDATE) without committing.
  autocommit=False, # If changes are to persist, they must be committed; no exceptions
  future=True
)
