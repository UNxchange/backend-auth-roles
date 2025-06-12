# app/db/models.py
from sqlalchemy import Column, Integer, String, Enum
from .database import Base
import enum

class UserRole(str, enum.Enum):
    estudiante = "estudiante"
    profesional = "profesional"
    administrador = "administrador"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False) # name prueba
    role = Column(String, nullable=False, default=UserRole.estudiante.value)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # role = Column(Enum(UserRole), nullable=False, default=UserRole.estudiante)
    # Podríamos añadir más campos como: full_name, is_active, etc.