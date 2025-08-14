from datetime import datetime

from auth.dtos.user_dto import (
    CreateUsuarioDTO
)
from auth.models.user_model import UsuarioModel

from auth.utils.managers import PasswordManager


class UserFactory:
    @staticmethod
    def create_user_from_create_dto(data: CreateUsuarioDTO) -> UsuarioModel:

        return UsuarioModel(
            email=data.email,
            id_rol=data.id_rol,
            cedula=data.cedula,
            nombres=data.nombres,
            apellidos=data.apellidos,
            celular=data.celular,
            bool_status=data.bool_status,
            contrasena=PasswordManager.hash_password(data.contrasena),
            created_at=datetime.now(),
            updated_at=None,
            deleted_at=None
        )
