from typing import List
from sqlalchemy.orm import Session

from auth.dtos.user_dto import (
    UsuarioDTO,
    CreateUsuarioDTO
)
from auth.factory import UserFactory
from auth.repository import UserRepository
from auth.utils.decorators import clean_fields


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    @clean_fields(['contrasena'])
    async def get_all(self) -> List[UsuarioDTO]:
        users = await self.repository.get_all()

        # Serialize sqlalchemy model to pydantic schema
        users = [
            UsuarioDTO.model_validate(usuario) for usuario in users]

        return users

    async def find_by_email(self, email: str) -> UsuarioDTO:
        user = await self.repository.find_by_email(email)

        if user is None:
            return []

        # Serialize sqlalchemy model to pydantic schema
        user = UsuarioDTO.model_validate(user)

        return user

    async def create(self, data: CreateUsuarioDTO) -> UsuarioDTO:
        try:
            # Verificar que no se repita el `email`
            user_retrieved_email = await self.find_by_email(data.email)

            # Validar duplicados
            if user_retrieved_email != []:
                return "US0003"  # Código de error para `email` duplicado

            # Crear la entidad para insertar
            user_data = UserFactory.create_user_from_create_dto(data)

            # Ejecutar la inserción en la base de datos
            user_post = await self.repository.create_user(user_data)

            user_post = UsuarioDTO.model_validate(user_post)

        except Exception as e:
            print(e)
            return "US9999"
        else:
            return user_post
