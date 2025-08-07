from sqlalchemy.orm import Session
from typing import List
from models.auth.user_model import UsuarioModel, RolUsuarioModel
from dtos.auth.user_dto import CreateUsuarioDTO, UsuarioDTO


class UserRepository:
    async def get_all(self, db: Session) -> List[UsuarioModel]:
        return db.query(UsuarioModel).all()

    async def find_by_email(self, db: Session, email: str) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.email == email).first()

    async def create_user(self, db: Session, user_data: UsuarioModel):
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        db.commit()

        return user_data


user_repository = UserRepository()
