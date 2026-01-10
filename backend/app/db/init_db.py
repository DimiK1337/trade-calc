# app/db/init_db.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.crud.user import get_by_email, create as create_user
from app.models.user import User


def ensure_admin_exists() -> None:
    """Fail fast if the DB has no admin user."""
    db: Session = SessionLocal()
    try:
        admin = db.scalar(select(User).where(User.is_admin.is_(True)).limit(1))
        if not admin:
            raise RuntimeError(
                "No admin user exists. Set ROOT_ADMIN_* env vars or create an admin in the DB."
            )
    finally:
        db.close()


def bootstrap_root_admin() -> None:
    """Idempotently create/promote root admin if env vars are present."""
    if not (
        settings.ROOT_ADMIN_EMAIL
        and settings.ROOT_ADMIN_USERNAME
        and settings.ROOT_ADMIN_PASSWORD
    ):
        print("NO ADMIN CREDENTIALS IN ENV/SETTINGS")
        return

    db: Session = SessionLocal()
    try:
        user = get_by_email(db, settings.ROOT_ADMIN_EMAIL)
        if user:
            if not user.is_admin:
                user.is_admin = True
                db.commit()
            return

        user = create_user(
            db=db,
            email=settings.ROOT_ADMIN_EMAIL,
            username=settings.ROOT_ADMIN_USERNAME,
            password=settings.ROOT_ADMIN_PASSWORD,
        )
        user.is_admin = True
        db.commit()
    finally:
        db.close()
