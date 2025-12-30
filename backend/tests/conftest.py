import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.deps import get_db
from app.db.base import Base
from app.main import app


@pytest.fixture(scope="session")
def test_db_url(tmp_path_factory: pytest.TempPathFactory) -> str:
    # one DB file for the whole test session
    p: Path = tmp_path_factory.mktemp("db") / "test.db"
    return f"sqlite:///{p}"


@pytest.fixture(scope="session")
def engine(test_db_url: str):
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    """
    New DB session per test; roll back anything not committed.
    (We also fully reset tables between tests for isolation.)
    """
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = TestingSessionLocal()

    # Clean tables for each test (simple + reliable for MVP scale)
    # If you add FK constraints later, you may need a smarter reset strategy.
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    # Override app dependency so API uses our test DB session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
