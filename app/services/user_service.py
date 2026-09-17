from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdatePartial



def create_user(db: Session, data: UserCreate):
    user = User(
        name=data.name,
        email=data.email,
        role=data.role.value if hasattr(data.role, "value") else data.role,
        is_active=data.is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def get_users(db: Session):
    return db.execute(select(User)).scalars().all()


def get_user(db: Session, user_id: int):
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()



def update_user(db: Session, user_id: int, data: UserCreate):
    user = get_user(db, user_id)
    if not user:
        return None

    user.name = data.name
    user.email = data.email
    user.role = data.role.value if hasattr(data.role, "value") else data.role
    user.is_active = data.is_active

    db.commit()
    db.refresh(user)
    return user



def update_user_partial(db: Session, user_id: int, data: UserUpdatePartial):
    user = get_user(db, user_id)
    if not user:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "role" and hasattr(value, "value"):
            value = value.value
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user



def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user



def filter_users_by_role(db: Session, role: str):
    return db.execute(select(User).where(User.role == role)).scalars().all()



def filter_users_by_status(db: Session, is_active: bool):
    return db.execute(select(User).where(User.is_active == is_active)).scalars().all()


def order_users_by_name(db: Session, asc: bool = True):
    order = User.name.asc() if asc else User.name.desc()
    return db.execute(select(User).order_by(order)).scalars().all()



def order_users_by_created(db: Session, asc: bool = True):
    order = User.created_at.asc() if asc else User.created_at.desc()
    return db.execute(select(User).order_by(order)).scalars().all()
