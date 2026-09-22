from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: RoleEnum = RoleEnum.user
    is_active: bool = True


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: RoleEnum
    is_active: bool


class UserUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)