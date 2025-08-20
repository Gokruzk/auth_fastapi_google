from datetime import datetime, timedelta
from typing import Annotated, List

import jwt
from fastapi import Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from auth.dtos.general_dto import ResponseSchema, TokenData
from auth.utils.messages import APP_MESSAGES
from auth.utils.timezone_utils import TimezoneUtils
from config import JWTConfig

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ----------------------------
# Password manager
# ----------------------------
class PasswordManager:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


# ----------------------------
# Responses's manager
# ----------------------------
class ResponsesManager:
    """
    Class to centralize responses
    """

    @staticmethod
    def success(**kwargs):
        if "data" in kwargs:
            return Response(
                ResponseSchema(
                    detail=APP_MESSAGES[kwargs["message_key"]]["detail"],
                    result=kwargs["data"],
                ).model_dump_json(),
                status_code=APP_MESSAGES[kwargs["message_key"]]["status_code"],
                media_type="application/json",
            )
        else:
            return Response(
                ResponseSchema(
                    detail=APP_MESSAGES[kwargs["message_key"]]["detail"],
                ).model_dump_json(),
                status_code=APP_MESSAGES[kwargs["message_key"]]["status_code"],
                media_type="application/json",
            )

    @staticmethod
    def error(message_key):
        return Response(
            ResponseSchema(
                detail=APP_MESSAGES[message_key]["detail"],
            ).model_dump_json(),
            status_code=APP_MESSAGES[message_key]["status_code"],
            media_type="application/json",
        )


class TokenManager:
    """
    Class to manage tokens
    """
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = TimezoneUtils.now_for_database(
        ) + timedelta(minutes=JWTConfig.token_expire())
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            JWTConfig.secret_key(),
            algorithm=JWTConfig.alogrithm()
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                JWTConfig.secret_key(),
                algorithms=[JWTConfig.alogrithm()]
            )
        except jwt.ExpiredSignatureError:
            return ResponsesManager.error(APP_MESSAGES["token_expired"])
        except jwt.InvalidTokenError:
            return ResponsesManager.error(APP_MESSAGES["invalid_token"])

    @classmethod
    def verify_token(cls, token: str = Depends(oauth2_scheme)) -> TokenData:
        try:
            payload = cls.decode_token(token)
            email: str = payload.get("email")
            role: str = payload.get("role")
            id_usuario: int = payload.get("id_usuario")
            exp: int = payload.get("exp")

            if not email or not role:
                return ResponsesManager.error(APP_MESSAGES["token_expired"])

            if exp and datetime.fromtimestamp(exp, tz=TimezoneUtils.ECUADOR_TZ) < TimezoneUtils.now_for_database():
                return ResponsesManager.error(APP_MESSAGES["invalid_token"])

            return TokenData(email=email, role=role, id_usuario=id_usuario)
        except Exception as e:
            print(f"Error verificando token: {e}")
            return ResponsesManager.error(APP_MESSAGES["unauthorized"])


class SessionManager:
    """
    Class to manage sessions and roles
    """
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
            return ResponsesManager.error(APP_MESSAGES["unexpected_error"])

    @staticmethod
    def rol_checker(allowed_roles: List[str]):
        def checker(token_data: TokenData = Depends(TokenManager.verify_token)) -> TokenData:
            if token_data.role not in allowed_roles:
                return ResponsesManager.error(APP_MESSAGES["forbidden"])
            return token_data
        return checker
