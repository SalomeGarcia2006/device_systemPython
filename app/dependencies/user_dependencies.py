from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user_model import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not isinstance(email, str):
            raise credentials_exception
    except (ValueError, TypeError):
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está inactivo",
        )
    return current_user


def require_roles(*allowed_roles: str) -> Callable:
    def validate_role(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )
        return current_user

    return validate_role


require_admin = require_roles("admin")
require_admin_or_support = require_roles("admin", "support")