from sqlalchemy.orm import Session
from typing import List
from models.user_model import UsuarioModel, RolUsuarioModel
from dtos.auth.user_dto import CreateUsuario, Usuario


class UserRepository:
    async def get_all(self, db: Session) -> List[UsuarioModel]:
        return db.query(UsuarioModel).all()

    async def find_by_email(self, db: Session, email: str) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.email==email).first()

    async def create_user(self, user_data: CreateUsuario):
        pass


user_repository = UserRepository()
