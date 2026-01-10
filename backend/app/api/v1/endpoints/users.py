# app/api/v1/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin, get_current_user
from app.crud.user import get_by_username, get_by_email, update_user, delete_user, change_password

from app.schemas.user import UserAdminOut, UserOut, UserUpdate, DeleteAccount, PasswordChange
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserAdminOut])
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    stmt = select(User).order_by(User.id.asc())
    return db.scalars(stmt).all()

@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserOut)
def patch_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Username change
    if payload.username is not None and payload.username != current_user.username:
        existing = get_by_username(db, payload.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")

    # Email change (require password)
    if payload.email is not None and payload.email != current_user.email:
        if not payload.current_password:
            raise HTTPException(status_code=400, detail="Current password required to change email")
        existing = get_by_email(db, payload.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # verify password using your existing auth verify
        from app.core.security import verify_password
        if not verify_password(payload.current_password, current_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid current password")

    return update_user(db, current_user, email=payload.email, username=payload.username)

@router.post("/me/password", status_code=204)
def update_my_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        change_password(db, current_user, current_password=payload.current_password, new_password=payload.new_password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid current password")
    return None


@router.delete("/me", status_code=204)
def delete_my_account(
    payload: DeleteAccount,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_user(db, current_user, current_password=payload.current_password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid current password")
    return None