import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.user_schema import RoleEnum


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: RoleEnum = RoleEnum.user
    is_active: bool = True

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if any(character.isspace() for character in value):
            raise ValueError("La contraseña no puede contener espacios en blanco")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe incluir al menos una mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe incluir al menos una minúscula")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe incluir al menos un número")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[EmailStr] = None

    model_config = ConfigDict(from_attributes=True)