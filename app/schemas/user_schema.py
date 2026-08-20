from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    is_active: bool = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool = True