"""
Alembic environment configuration.

This file tells Alembic:
- how to connect to the database
- where to find SQLAlchemy metadata (tables)
- how to run migrations (offline vs online)

If migrations are not detected or are empty, the problem is almost
always in this file.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Application settings (DATABASE_URL lives here)
from app.core.config import settings

# SQLAlchemy Base that holds metadata for *all* ORM models
from app.db.base import Base

# IMPORTANT:
# Importing models ensures that all ORM classes are registered
# on Base.metadata before Alembic inspects it.
#
# Without this import, Alembic will think there are no tables
# and autogenerate empty migrations.
from app import models  # noqa: F401


# Alembic Config object (reads alembic.ini)
config = context.config

# Configure logging using alembic.ini
# This enables Alembic log output (INFO messages you see in terminal)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# This is the metadata Alembic will scan when autogenerating migrations.
# It must be Base.metadata, not None.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in "offline" mode.

    Offline mode does NOT create a DB connection.
    Alembic instead generates raw SQL scripts.

    This is useful for:
    - generating SQL files
    - environments where DB access is restricted

    For normal dev usage, online mode is used instead.
    """
    context.configure(
        url=settings.DATABASE_URL,          # DB URL (from .env)
        target_metadata=target_metadata,    # tables to migrate
        literal_binds=True,                 # render actual values in SQL
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in "online" mode.

    Online mode:
    - creates an actual DB connection
    - applies migrations directly to the database
    - this is what `alembic upgrade head` uses
    """

    # Override sqlalchemy.url in alembic.ini using our settings
    # This ensures Alembic always uses the same DB as the app
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    # Create SQLAlchemy engine from Alembic config
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # no connection pooling for migrations
    )

    # Open DB connection and associate it with Alembic
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Decide which mode to use
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
