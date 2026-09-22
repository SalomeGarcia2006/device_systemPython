from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.core.security import create_access_token
from app.database import get_db
from app.dependencies.user_dependencies import get_current_active_user
from app.models.user_model import User
from app.schemas.auth_schema import Token, UserRegister
from app.schemas.user_schema import UserResponse
from app.services.auth_service import authenticate_user, register_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya existe")
    return user


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseÃ±a incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El usuario estÃ¡ inactivo")
    return Token(access_token=create_access_token({"sub": user.email, "role": user.role}))


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user