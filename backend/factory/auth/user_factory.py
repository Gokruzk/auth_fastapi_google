from datetime import datetime

from dtos.auth.user_dto import (
    Usuario
)
from utils.auth import get_password_hash


class UserFactory:
    pass
    # @staticmethod
    # def create_user_from_create_dto(data: CreateUserDTO):

    #     return {
    #         "email": data.email,
    #         "id_rol": data.id_rol,
    #         "cedula": data.cedula,
    #         "nombre": data.nombre,
    #         "apellido": data.apellido,
    #         "genero": data.genero,
    #         "contrasena": get_password_hash(data.contrasena),
    #         "esta_conectado": data.esta_conectado,
    #         "fue_eliminado": data.fue_eliminado,
    #         "fecha_creacion": datetime.now(),
    #     }

    # @staticmethod
    # def fetch_user(user: Usuario):
    #     return Usuario(
    #         email=user.email,
    #         id_rol=user.id_rol,
    #         cedula=user.cedula,
    #         nombres=user.nombres,
    #         apellidos=user.apellidos,
    #         created_at=user.created_at,
    #         updated_at=user.updated_at
    #     )

    # @staticmethod
    # def create_user_password_updated(
    #     data: UpdateUserPasswordDTO,
    # ) -> UpdateUserPasswordDTO:
    #     return {
    #         "id_usuario": data["id_usuario"],
    #         "contrasena": get_password_hash(data["contrasena"]),
    #     }

    # @staticmethod
    # def to_delete(fue_eliminado: bool):
    #     return {
    #         "fue_eliminado": fue_eliminado,
    #         "fecha_eliminacion": datetime.now(),
    #     }
