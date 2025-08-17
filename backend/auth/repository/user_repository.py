from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from auth.models import UsuarioModel


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[UsuarioModel]:
        result = await self.db.execute(select(UsuarioModel))
        return result.scalars().all()

    async def find_by_email(self, email: str) -> Optional[UsuarioModel]:
        result = await self.db.execute(
            select(UsuarioModel)
            .options(selectinload(UsuarioModel.rol))  # carga relación
            .where(UsuarioModel.email == email)
        )
        return result.scalars().first()

    async def create_user(self, user_data: UsuarioModel) -> UsuarioModel:
        self.db.add(user_data)
        await self.db.commit()
        await self.db.refresh(user_data)
        return user_data
