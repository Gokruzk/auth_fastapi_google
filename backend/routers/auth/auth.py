import uuid
from datetime import timedelta, datetime
from os import getenv
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from dtos.auth.user_dto import UserDTO
from dtos.general_dto import (
    RecoverPasswordDTO,
    ResponseSchema,
    Role,
    Token,
    UpdatePasswordDTO,
    ValidateResetCodeDTO,
)
from services.auth.user_service import UserService
from utils.authorization import create_access_token, role_required, verify_password
from utils.messages.auth import APP_MESSAGES

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
DATABASE_URL = getenv("DATABASE_URL")


@router.post(
    path="/login",
    response_model=Token,
)
async def auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """# Buscar el usuario
    if form_data.username == "ferchon123443@gmail.com":
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={
                "email": "ferchon12344@gmail.com",
                "role": "2",
                "id_usuario": 2,
                "nombre": "Fernando",
            },
            expires_delta=access_token_expires,
        )

        return Token(access_token=access_token, token_type="bearer")"""
    user_data: UserDTO = await UserService.find_by_email(form_data.username)
    # Determinar el objeto del usuario autenticado
    authenticated_user = None

    if user_data:  # Si user_data no es vacío
        authenticated_user: UserDTO = user_data
        if user_data.id_rol == 2:
            # Verificar membresía
            membership_status = await UserService.verify_membership(
                user_data.id_usuario
            )

            if membership_status == "US0006":  # Si la membresía no está activa
                raise HTTPException(
                    status_code=APP_MESSAGES["need_memb"]["status_code"],
                    detail=APP_MESSAGES["need_memb"]["detail"],
                    headers={"WWW-Authenticate": "Bearer"},
                )

        if authenticated_user.fue_eliminado is True:
            raise HTTPException(
                status_code=APP_MESSAGES["account_disabled"]["status_code"],
                detail=APP_MESSAGES["account_disabled"]["detail"],
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Si no se encuentra el usuario
    if not authenticated_user:
        raise HTTPException(
            status_code=APP_MESSAGES["user_not_found"]["status_code"],
            detail=APP_MESSAGES["user_not_found"]["detail"],
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar la contraseña
    if not verify_password(form_data.password, authenticated_user.contrasena):
        raise HTTPException(
            status_code=APP_MESSAGES["incorrect_email_psw"]["status_code"],
            detail=APP_MESSAGES["incorrect_email_psw"]["detail"],
            headers={"WWW-Authenticate": "Bearer"},
        )

    if authenticated_user:
        await UserService.set_online(
            {"email": authenticated_user.email, "esta_conectado": True}
        )

    # Crear el token de acceso
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={
            "email": authenticated_user.email,
            "role": user_data.rol_usuario.rol,
            "id_usuario": user_data.id_usuario,
            "nombre": user_data.nombre,
        },
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
