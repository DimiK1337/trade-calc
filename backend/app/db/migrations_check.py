from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine

from app.core.config import settings


def ensure_db_is_at_head() -> None:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current = context.get_current_revision()

    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    head = script.get_current_head()

    if current != head:
        raise RuntimeError(
            f"Database is not up to date. Current={current}, Head={head}. "
            f"Run: alembic upgrade head"
        )
