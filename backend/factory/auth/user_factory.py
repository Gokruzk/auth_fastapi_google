from datetime import datetime

from dtos.auth.user_dto import (
    UsuarioDTO,
    CreateUsuarioDTO
)
from models.auth.user_model import UsuarioModel

from utils.auth import get_password_hash


class UserFactory:
    @staticmethod
    def create_user_from_create_dto(data: CreateUsuarioDTO):

        return UsuarioModel(
            email=data.email,
            id_rol=data.id_rol,
            cedula=data.cedula,
            nombres=data.nombres,
            apellidos=data.apellidos,
            celular=data.celular,
            bool_status=data.bool_status,
            contrasena=get_password_hash(data.contrasena),
            created_at=datetime.now(),
            updated_at=None,
            deleted_at=None
        )
