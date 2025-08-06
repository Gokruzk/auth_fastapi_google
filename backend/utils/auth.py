from datetime import datetime, timedelta
from os import getenv
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from dtos.general_dto import ResponseSchema, Role, TokenData
from utils.messages.auth import APP_MESSAGES
from utils.timezone_utils import TimezoneUtils

SECRET_KEY = getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = TimezoneUtils.now_for_database() + expires_delta
    else:
        expire = TimezoneUtils.now_for_database() + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    from services.auth.user_service import UserService

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        email: str = payload.get("email")
        role: str = payload.get("role")

        if not email or not role:
            raise HTTPException(
                status_code=APP_MESSAGES["invalid_credentials"]["status_code"],
                detail=APP_MESSAGES["invalid_credentials"]["detail"],
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif email is None or type is None:
            raise HTTPException(
                status_code=APP_MESSAGES["could_not_valid_credentials"]["status_code"],
                detail=APP_MESSAGES["could_not_valid_credentials"]["detail"],
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = TokenData(email=email, role=role)
        user = await UserService.find_by_email(token_data.email)

        if user == []:
            raise HTTPException(
                status_code=APP_MESSAGES["user_not_found"]["status_code"],
                detail=APP_MESSAGES["user_not_found"]["detail"],
                headers={"WWW-Authenticate": "Bearer"},
            )

    except HTTPException as e:
        raise e
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=APP_MESSAGES["token_expired"]["status_code"],
            detail=APP_MESSAGES["token_expired"]["detail"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=APP_MESSAGES["invalid_token"]["status_code"],
            detail=APP_MESSAGES["invalid_token"]["detail"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(e)
        return Response(
            ResponseSchema(
                detail="An unexpected error occurred").model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json",
        )
    else:
        return token_data


def verify_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Verifica y decodifica el token JWT
    """
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extraer datos del token
        email: str = payload.get("email")
        role: str = payload.get("role")
        id_usuario: int = payload.get("id_usuario")
        exp: int = payload.get("exp")

        if not email or not role:
            raise HTTPException(**APP_MESSAGES["invalid_token"])

        # Verificar expiración
        if (
            exp
            and datetime.fromtimestamp(exp, tz=TimezoneUtils.ECUADOR_TZ)
            < TimezoneUtils.now_for_database()
        ):
            raise HTTPException(**APP_MESSAGES["token_expired"])

        # Crear objeto TokenData
        token_data = TokenData(email=email, role=role, id_usuario=id_usuario)

        return token_data

    except jwt.ExpiredSignatureError:
        raise HTTPException(**APP_MESSAGES["token_expired"])
    except jwt.InvalidTokenError:
        raise HTTPException(**APP_MESSAGES["invalid_token"])
    except Exception as e:
        print(f"Error verificando token: {e}")
        raise HTTPException(**APP_MESSAGES["unauthorized"])


def user_required(token_data: TokenData = Depends(verify_token)):
    """
    Verificar que el rol sea de usuario
    """
    if token_data.role != Role.user.value:
        raise HTTPException(**APP_MESSAGES["forbidden"])
    return token_data


def admin_required(token_data: TokenData = Depends(verify_token)):
    """
    Verificar que el usuario sea administrador
    """
    if token_data.role not in [Role.admin.value]:
        raise HTTPException(**APP_MESSAGES["forbidden"])
    return token_data


def any_authenticated_user(token_data: TokenData = Depends(verify_token)):
    """
    Verificar que el usuario esté autenticado (cualquier rol válido)
    """
    if token_data.role not in [Role.admin.value, Role.user.value]:
        raise HTTPException(**APP_MESSAGES["invalid_role"])
    return token_data
