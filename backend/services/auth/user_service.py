from typing import List
from sqlalchemy.orm import Session

from dtos.auth.user_dto import (
    Usuario
)
from factory.auth.user_factory import UserFactory
from repository.auth.user_repository import user_repository
from utils.auth import get_password_hash, verify_password
from utils.decorators import clean_fields


class UserService:
    @staticmethod
    async def get_all(db: Session) -> List[Usuario]:
        users = await user_repository.get_all(db)

        # Serialize sqlalchemy model to pydantic schema
        users = [
            Usuario.model_validate(usuario) for usuario in users]

        return users

    # @staticmethod
    # async def create(data: CreateUserDTO) -> UserDTO:
    #     try:
    #         # Verificar que no se repita el `email`
    #         user_retrieved_email = await UserService.find_by_email(data.email)

    #         # Validar duplicados
    #         if user_retrieved_email != []:
    #             return "US0004"  # Código de error para `email` duplicado

    #         # Crear la entidad para insertar
    #         user_data = UserFactory.create_user_from_create_dto(data)

    #         # Ejecutar la inserción en la base de datos
    #         user_post = await user_repository.create_user(user_data)

    #     except Exception as e:
    #         print(e)
    #         return "US9999"
    #     else:
    #         return user_post
