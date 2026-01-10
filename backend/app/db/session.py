# app/db/session.py

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from app.core.config import settings

# SQLite needs this in multithreaded apps (FastAPI dev server)
isDB_SQLite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if isDB_SQLite  else {}

engine = create_engine(
  settings.DATABASE_URL, 
  connect_args=connect_args, 
  future=True
)

if isDB_SQLite:
  @event.listens_for(Engine, "connect")
  def _set_sqlite_pragma(dbapi_connection, connection_record):
      cursor = dbapi_connection.cursor()
      cursor.execute("PRAGMA foreign_keys=ON")
      cursor.close()

SessionLocal = sessionmaker(
  bind=engine, 
  autoflush=False, # “Flush” means: send pending changes to the DB (INSERT/UPDATE) without committing.
  autocommit=False, # If changes are to persist, they must be committed; no exceptions
  future=True
)
