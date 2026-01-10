# app/api/v1/endpoints/profile.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.security import verify_password
from app.crud.user import (
    get_by_email,
    get_by_username,
    update_user,
    change_password,
    delete_user,
)
from app.schemas.user import UserOut, UserUpdate, PasswordChange, DeleteAccount
from app.models.user import User

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserOut)
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("", response_model=UserOut)
def update_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.username is not None and payload.username != current_user.username:
        existing = get_by_username(db, payload.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")

    if payload.email is not None and payload.email != current_user.email:
        if not payload.current_password:
            raise HTTPException(status_code=400, detail="Current password required to change email")
        existing = get_by_email(db, payload.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        if not verify_password(payload.current_password, current_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid current password")

    return update_user(db, current_user, email=payload.email, username=payload.username)


@router.post("/password", status_code=204)
def update_profile_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        change_password(
            db,
            current_user,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid current password")
    return None


@router.delete("", status_code=204)
def delete_profile(
    payload: DeleteAccount,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_user(db, current_user, current_password=payload.current_password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid current password")
    return None
