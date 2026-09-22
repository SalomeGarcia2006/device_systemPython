from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister


def register_user(db: Session, data: UserRegister) -> User | None:
    if db.query(User).filter(User.email == str(data.email)).first():
        return None

    user = User(
        name=data.name,
        email=str(data.email),
        hashed_password=get_password_hash(data.password),
        # Public registration must not allow privilege escalation.
        role="user",
        is_active=data.is_active,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return None
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user