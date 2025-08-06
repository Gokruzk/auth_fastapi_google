from sqlalchemy.orm import Session
from typing import List
from models.user_model import Usuario, RolUsuario


class UserRepository:
    async def get_all(self, db: Session):
        return db.query(Usuario).all()

    # async def find_by_email(self, email: str) -> Usuario:
    #     return await conn.prisma.usuario.find_unique_or_raise(
    #         where={"email": email}, include={"rol_usuario": True}
    #     )

    # async def create_user(self, user_data: CreateUsuario) -> Usuario:
    #     # Prepare data for creation
    #     processed_data = user_data
    #     return await conn.prisma.usuario.create(data=processed_data)


user_repository = UserRepository()
