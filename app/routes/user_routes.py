from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.schemas.user_schema import UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


# Lista de usuarios
users = [
    {
        "id": 1,
        "name": "Administrador",
        "email": "admin@devicesystems.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Soporte",
        "email": "support@devicesystems.com",
        "role": "support",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Usuario",
        "email": "user@devicesystems.com",
        "role": "user",
        "is_active": False
    }
]


# GET /users
# Obtener todos los usuarios
@router.get("", response_model=list[UserResponse])
def get_users(
    role: Optional[str] = Query(default=None),
    is_active: Optional[bool] = Query(default=None)
):

    result = users

    # Filtrar por rol
    if role is not None:
        result = [
            user for user in result
            if user["role"] == role
        ]

    # Filtrar por estado
    if is_active is not None:
        result = [
            user for user in result
            if user["is_active"] == is_active
        ]

    return result


# GET /users/{user_id}
# Obtener un usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )