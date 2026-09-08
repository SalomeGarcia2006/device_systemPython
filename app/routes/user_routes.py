from fastapi import APIRouter, HTTPException, Query, Response
from typing import Optional

from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


# Lista de usuarios JSON simulada
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



# GET - Buscar usuario por ID

@router.get("/{id}")
def buscar_usuario(id: int):
    for user in users:
        if user["id"] == id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# GET - Todos los usuarios


@router.get("")
def buscar_todos_los_usuarios():
    return users



# GET - Filtrar usuarios por rol


@router.get("/")
def buscar_rol(role: str = Query(...)):
    usuarios = []

    for user in users:
        if user["role"] == role:
            usuarios.append(user)

    return usuarios



# GET - Filtrar usuarios por estado


@router.get("/estado/estado")
def get_usuarios_por_estado(is_active: bool = Query(...)):
    usuarios_filtrados = [
        u for u in users
        if u["is_active"] == is_active
    ]

    if not usuarios_filtrados:
        raise HTTPException(
            status_code=404,
            detail="No hay usuarios con ese estado"
        )

    return usuarios_filtrados



# POST - Crear usuario


@router.post("/", response_model=UserResponse)
def crear_usuario(
    usuario: UserCreate,
    response: Response
):
    # Verificar correo duplicado
    for user in users:
        if user["email"] == usuario.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    # Crear nuevo usuario
    nuevo_usuario = {
        "id": len(users) + 1,
        "name": usuario.name,
        "email": usuario.email,
        "role": usuario.role,
        "is_active": usuario.is_active
    }

    users.append(nuevo_usuario)

    # Cabeceras personalizadas
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    return nuevo_usuario




#PUT
@router.put("/{id}", response_model=UserResponse)
def actualizar_usuario(id: int, usuario: UserCreate):
    for user in users:
        if user["id"] == id:
            user["name"] = usuario.name
            user["email"] = usuario.email
            user["role"] = usuario.role
            user["is_active"] = usuario.is_active

            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# Patch 


@router.patch("/{id}", response_model=UserResponse)
def actualizar_parcialmente_usuario(id: int, usuario: UserUpdate):
    for user in users:
        if user["id"] == id:

            datos_actualizados = usuario.model_dump(exclude_unset=True)

            if not datos_actualizados:
                raise HTTPException(
                    status_code=400,
                    detail="No se enviaron campos para actualizar"
                )

            user.update(datos_actualizados)

            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )