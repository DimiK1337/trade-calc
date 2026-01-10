# app/crud/user.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalars().first()

def get_by_username(db: Session, username: str) -> User | None:
    return db.execute(select(User).where(User.username == username)).scalars().first()

def get_by_id(db: Session, id: str) -> User | None:
    return db.execute(select(User).where(User.id == id)).scalars().first()

def create(db: Session, email: str, username: str, password: str) -> User:
    print(f"In crud/user.py, {email = } {username = } {password = }")
    user = User(email=email, password_hash=hash_password(password), username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, *, email: str | None, username: str | None) -> User:
    if email is not None:
        user.email = email
    if username is not None:
        user.username = username
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def change_password(db: Session, user: User, *, current_password: str, new_password: str) -> None:
    if not verify_password(current_password, user.password_hash):
        raise ValueError("Invalid current password")
    user.password_hash = hash_password(new_password)
    db.add(user)
    db.commit()

def delete_user(db: Session, user: User, *, current_password: str) -> None:
    if not verify_password(current_password, user.password_hash):
        raise ValueError("Invalid current password")
    db.delete(user)
    db.commit()

