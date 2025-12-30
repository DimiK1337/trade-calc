from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create(db: Session, email: str, username: str, password: str) -> User:
    print(f"In crud/user.py, {email = } {username = } {password = }")
    user = User(email=email, password_hash=hash_password(password), username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
