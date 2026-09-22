from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.database import get_db
from app.dependencies.user_dependencies import get_current_active_user, require_admin
from app.schemas.loan_schema import LoanResponse
from app.schemas.auth_schema import UserRegister
from app.schemas.user_schema import UserUpdate, UserUpdatePartial, UserResponse
from app.services.loan_service import get_user_loans
from app.services.user_service import (
    create_user,
    delete_user,
    get_user,
    get_users,
    update_user,
    update_user_partial,
)


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse], summary="Listar usuarios")
@limiter.limit("30/minute")
def list_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return get_users(db)


@router.get("/{user_id}/loans", response_model=list[LoanResponse], summary="Consultar prÃ©stamos de un usuario")
def user_loans(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return get_user_loans(db, user_id)


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/", response_model=UserResponse, status_code=201, summary="Crear usuario")
def create_user_route(
    data: UserRegister,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = create_user(db, data)
    if user is None:
        raise HTTPException(status_code=409, detail="El email ya existe")
    return user


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario")
def update_user_route(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = update_user(db, user_id, data)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user == "duplicate":
        raise HTTPException(status_code=409, detail="El email ya existe")
    return user


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar parcialmente un usuario")
def update_user_partial_route(
    user_id: int,
    data: UserUpdatePartial,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = update_user_partial(db, user_id, data)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user == "duplicate":
        raise HTTPException(status_code=409, detail="El email ya existe")
    return user


@router.delete("/{user_id}", summary="Eliminar usuario")
def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user == "conflict":
        raise HTTPException(status_code=409, detail="No se puede eliminar un usuario con prÃ©stamos asociados")
    return {"message": "Usuario eliminado correctamente"}