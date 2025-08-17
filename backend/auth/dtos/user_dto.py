from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date, datetime


class BaseDTO(BaseModel):

    class Config:
        from_attributes = True


class RolUsuarioDTO(BaseDTO):
    id_rol: int
    rol: str


class UsuarioDTO(BaseDTO):
    email: EmailStr
    cedula: str
    nombres: str
    apellidos: str
    celular: str
    contrasena: str
    bool_status: bool
    created_at: datetime
    updated_at: Optional[date]
    deleted_at: Optional[date]
    id_rol: int


class RUsuarioDTO(UsuarioDTO):
    rol: RolUsuarioDTO


class CreateUsuarioDTO(BaseDTO):
    email: str
    cedula: str
    nombres: str
    apellidos: str
    celular: str
    bool_status: bool
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None
    id_rol: int
    contrasena: str
