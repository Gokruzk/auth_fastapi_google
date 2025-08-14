from sqlalchemy.orm import Session
from typing import List
from auth.models.user_model import UsuarioModel, RolUsuarioModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[UsuarioModel]:
        return self.db.query(UsuarioModel).all()

    async def find_by_email(self, email: str) -> UsuarioModel:
        return self.db.query(UsuarioModel).filter(UsuarioModel.email == email).join(RolUsuarioModel).first()

    async def create_user(self, user_data: UsuarioModel):
        self.db.add(user_data)
        self.db.commit()
        self.db.refresh(user_data)
        self.db.commit()

        return user_data
