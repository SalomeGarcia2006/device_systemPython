from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserUpdatePartial


def create_user(db: Session, data: UserCreate):
    if get_user_by_email(db, str(data.email)):
        return None
    user = User(name=data.name, email=str(data.email), hashed_password=get_password_hash(data.password), role=data.role.value, is_active=data.is_active)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return None
    return user


def get_users(db: Session):
    return db.execute(select(User)).scalars().all()


def get_user(db: Session, user_id: int):
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    duplicate = db.execute(select(User).where(User.email == str(data.email), User.id != user_id)).scalar_one_or_none()
    if duplicate:
        return "duplicate"
    user.name, user.email, user.role, user.is_active = data.name, str(data.email), data.role.value, data.is_active
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return "duplicate"
    return user


def update_user_partial(db: Session, user_id: int, data: UserUpdatePartial):
    user = get_user(db, user_id)
    if not user:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if "email" in update_data:
        duplicate = db.execute(select(User).where(User.email == str(update_data["email"]), User.id != user_id)).scalar_one_or_none()
        if duplicate:
            return "duplicate"
    for key, value in update_data.items():
        setattr(user, key, value.value if key == "role" else str(value) if key == "email" else value)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return "duplicate"
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    if db.execute(select(Loan.id).where(Loan.user_id == user_id)).first():
        return "conflict"
    db.delete(user)
    db.commit()
    return user