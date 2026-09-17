from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserUpdatePartial,
    UserResponse,
)

from app.schemas.loan_schema import LoanResponse

from app.services.user_service import (
    create_user,
    get_users,
    get_user,
    update_user,
    update_user_partial,
    delete_user,
)

from app.services.loan_service import get_user_loans


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
)
def list_users(
    db: Session = Depends(get_db),
):
    return get_users(db)


@router.get(
    "/{user_id}/loans",
    response_model=list[LoanResponse],
    summary="Consultar préstamos de un usuario",
    description="Obtiene todos los préstamos asociados a un usuario.",
)
def user_loans(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    return get_user_loans(db, user_id)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario",
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    return user


@router.post(
    "/",
    response_model=UserResponse,
    summary="Crear usuario",
)
def create_user_route(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
)
def update_user_route(
    user_id: int,
    data: UserCreate,
    db: Session = Depends(get_db),
):
    user = update_user(db, user_id, data)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar parcialmente un usuario",
)
def update_user_partial_route(
    user_id: int,
    data: UserUpdatePartial,
    db: Session = Depends(get_db),
):
    user = update_user_partial(db, user_id, data)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    return user


@router.delete(
    "/{user_id}",
    summary="Eliminar usuario",
)
def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = delete_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    return {"message": "Usuario eliminado correctamente"}