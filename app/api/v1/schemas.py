# app/api/v1/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.models import UserRole

# Schema para la creación de un usuario
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.estudiante

# Schema para mostrar la info de un usuario (sin la contraseña)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        orm_mode = True # Permite que Pydantic lea datos desde modelos ORM

# Schema para el token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None