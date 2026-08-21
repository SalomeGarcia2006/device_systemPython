from fastapi import APIRouter, HTTPException, Query, Response
from typing import Optional

from app.schemas.user_schema import UserResponse, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


# Lista de usuarios json simulada
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
    response: Response,
    role: Optional[str] = Query(default=None),
    is_active: Optional[bool] = Query(default=None)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
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


# POST /users
# Crear un nuevo usuario


@router.post("", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):

    # Validar nombre
    if len(user.name) < 3:
        raise HTTPException(
            status_code=400,
            detail="El nombre debe tener mínimo 3 caracteres"
        )

    # Validar rol
    if user.role not in ["admin", "support", "user"]:
        raise HTTPException(
            status_code=400,
            detail="El rol debe ser admin, support o user"
        )

    # Verificar correo duplicado
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    # Crear nuevo ID
    new_id = len(users) + 1

    # Crear nuevo usuario
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

    # Guardar usuario
    users.append(new_user)

    return new_user