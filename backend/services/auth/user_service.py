from typing import List
from sqlalchemy.orm import Session

from dtos.auth.user_dto import (
    UsuarioDTO,
    CreateUsuarioDTO
)
from factory.auth.user_factory import UserFactory
from repository.auth.user_repository import user_repository
from utils.auth import get_password_hash, verify_password
from utils.decorators import clean_fields


class UserService:
    @staticmethod
    async def get_all(db: Session) -> List[UsuarioDTO]:
        users = await user_repository.get_all(db)

        # Serialize sqlalchemy model to pydantic schema
        users = [
            UsuarioDTO.model_validate(usuario) for usuario in users]

        return users

    @staticmethod
    async def find_by_email(db: Session, email: str) -> UsuarioDTO:
        user = await user_repository.find_by_email(db, email)

        if user is None:
            return []
        
        # Serialize sqlalchemy model to pydantic schema
        user = UsuarioDTO.model_validate(user)

        return user

    @staticmethod
    async def create(db: Session, data: CreateUsuarioDTO) -> UsuarioDTO:
        try:
            # Verificar que no se repita el `email`
            user_retrieved_email = await UserService.find_by_email(db, data.email)

            # Validar duplicados
            if user_retrieved_email != []:
                return "US0003"  # Código de error para `email` duplicado

            # Crear la entidad para insertar
            user_data = UserFactory.create_user_from_create_dto(data)

            # Ejecutar la inserción en la base de datos
            user_post = await user_repository.create_user(db, user_data)

            user_post = UsuarioDTO.model_validate(user_post)

        except Exception as e:
            print(e)
            return "US9999"
        else:
            return user_post
