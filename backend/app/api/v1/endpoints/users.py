# Admin only

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.schemas.user import UserAdminOut
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserAdminOut])
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    stmt = select(User).order_by(User.id.asc())
    return db.scalars(stmt).all()

