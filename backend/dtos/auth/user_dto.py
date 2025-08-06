from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class BaseDTO(BaseModel):

    class Config:
        from_attributes = True


class RolUsuarioDTO(BaseDTO):
    id_rol: int
    rol: str


class Usuario(BaseDTO):
    email: str
    cedula: str
    nombres: str
    apellidos: str
    celular: str
    bool_status: bool
    created_at: datetime
    updated_at: Optional[date]
    deleted_at: Optional[date]
    
    id_rol: int

class CreateUsuario(BaseDTO):
    email: str
    cedula: str
    nombres: str
    apellidos: str
    celular: str
    bool_status: bool
    created_at: datetime
    id_rol: int
