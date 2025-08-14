from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from auth.dtos.general_dto import ResponseSchema, Role, TokenData
from auth.utils.messages import APP_MESSAGES
from auth.utils.timezone_utils import TimezoneUtils
from config.config import JWTConfig

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ----------------------------
# Manejo de contraseñas
# ----------------------------
class PasswordManager:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


# ----------------------------
# Manejo de tokens JWT
# ----------------------------
class TokenManager:
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = TimezoneUtils.now_for_database(
        ) + (timedelta(minutes=JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES()))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, JWTConfig.SECRET_KEY(), algorithm=JWTConfig.ALGORITHM())
        return encoded_jwt

    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)) -> TokenData:
        try:
            payload = jwt.decode(token, JWTConfig.SECRET_KEY(), algorithms=[
                                 JWTConfig.ALGORITHM()])
            email: str = payload.get("email")
            role: str = payload.get("role")
            id_usuario: int = payload.get("id_usuario")
            exp: int = payload.get("exp")

            if not email or not role:
                raise HTTPException(**APP_MESSAGES["invalid_token"])

            if exp and datetime.fromtimestamp(exp, tz=TimezoneUtils.ECUADOR_TZ) < TimezoneUtils.now_for_database():
                raise HTTPException(**APP_MESSAGES["token_expired"])

            return TokenData(email=email, role=role, id_usuario=id_usuario)
        except jwt.ExpiredSignatureError:
            raise HTTPException(**APP_MESSAGES["token_expired"])
        except jwt.InvalidTokenError:
            raise HTTPException(**APP_MESSAGES["invalid_token"])
        except Exception as e:
            print(f"Error verificando token: {e}")
            raise HTTPException(**APP_MESSAGES["unauthorized"])


# ----------------------------
# Manejo de sesiones y permisos
# ----------------------------
class SessionManager:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
        from services.user_service import UserService

        try:
            token_data = TokenManager.verify_token(token)
            user = await UserService.find_by_email(token_data.email)
            if not user:
                raise HTTPException(**APP_MESSAGES["user_not_found"])
            return token_data
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error inesperado en get_current_user: {e}")
            return Response(
                ResponseSchema(
                    detail="An unexpected error occurred").model_dump_json(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                media_type="application/json",
            )

    @staticmethod
    def user_required(token_data: TokenData = Depends(TokenManager.verify_token)) -> TokenData:
        if token_data.role != Role.user.value:
            raise HTTPException(**APP_MESSAGES["forbidden"])
        return token_data

    @staticmethod
    def admin_required(token_data: TokenData = Depends(TokenManager.verify_token)) -> TokenData:
        if token_data.role != Role.admin.value:
            raise HTTPException(**APP_MESSAGES["forbidden"])
        return token_data

    @staticmethod
    def any_authenticated_user(token_data: TokenData = Depends(TokenManager.verify_token)) -> TokenData:
        if token_data.role not in [Role.admin.value, Role.user.value]:
            raise HTTPException(**APP_MESSAGES["invalid_role"])
        return token_data
