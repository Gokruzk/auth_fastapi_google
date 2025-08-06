from datetime import timedelta
from os import getenv
from typing import List
from sqlalchemy.orm import Session
from config.db import get_db

from fastapi import APIRouter, Depends, HTTPException, Path, Response

from models.user_model import Usuario as UsuarioSchema

from dtos.auth.user_dto import (
    # CreateDTO,
    # UserDTO,
    Usuario
)
from dtos.general_dto import ResponseSchema, Role, TokenData
from services.auth.user_service import UserService
from utils.auth import create_access_token, user_required, admin_required, any_authenticated_user
from utils.messages.auth import APP_MESSAGES

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


@router.post(
    path="/all", response_model=ResponseSchema, response_model_exclude_none=True
    # path="/all", response_model_exclude_none=True
)
async def get_all(
    # rol: int,
    # token_data: TokenData = Depends(any_authenticated_user),
    db: Session = Depends(get_db)
):
    try:
        # Obtener todos los usuarios
        data: List[Usuario] = await UserService.get_all(db)

        if data == "US9998":  # Mensaje de error
            raise HTTPException(
                **APP_MESSAGES["get_users_error"],
            )
        elif data == []:  # Si no hay usuarios
            raise HTTPException(**APP_MESSAGES["no_users_found"])

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(
            ResponseSchema(
                detail=APP_MESSAGES["unexpected_error"]["detail"]
            ).model_dump_json(),
            status_code=APP_MESSAGES["unexpected_error"]["status_code"],
            media_type="application/json",
        )
    else:
        return Response(
            ResponseSchema(
                detail=APP_MESSAGES["successfully_retrieved"]["detail"], result=data
            ).model_dump_json(),
            status_code=APP_MESSAGES["successfully_retrieved"]["status_code"],
            media_type="application/json",
        )


# @router.get(
#     path="/{email}", response_model=ResponseSchema, response_model_exclude_none=True
# )
# async def find_by_email(
#     email: str = Path(..., alias="email"),
#     token_data: TokenData = Depends(any_authenticated_user),
# ):
#     try:
#         # Obtener usuario por email
#         data: UserDTO = await UserService.find_by_email(email)

#         if data == "US9998":  # Mensaje de error
#             raise HTTPException(**APP_MESSAGES["get_user_error"])
#         elif data == []:  # Si no existe el usuario
#             raise HTTPException(**APP_MESSAGES["user_not_found"])

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(e)
#         return Response(
#             ResponseSchema(APP_MESSAGES["get_users_error"]).model_dump_json(),
#             status_code=APP_MESSAGES["get_users_error"]["status_code"],
#             media_type="application/json",
#         )
#     else:
#         return Response(
#             ResponseSchema(
#                 detail=APP_MESSAGES["successfully_retrieved"]["detail"], result=data
#             ).model_dump_json(),
#             status_code=APP_MESSAGES["successfully_retrieved"]["status_code"],
#             media_type="application/json",
#         )


# @router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
# async def create_user(new_user: CreateDTO):
#     try:
#         if new_user.id_rol == 2:
#             user_created: UserDTO = await UserService.create_client(new_user)
#         else:
#             user_created: UserDTO = await UserService.create(new_user)

#         if user_created == "US9999":  # Mensaje de error
#             raise HTTPException(**APP_MESSAGES["unexpected_error"])
#         elif user_created == "US0002":  # Si el username ya existe
#             raise HTTPException(**APP_MESSAGES["username_exists"])
#         elif user_created == "US0003":  # Si el dni ya existe
#             raise HTTPException(**APP_MESSAGES["dni_exists"])
#         elif user_created == "US0004":  # Si el email ya existe
#             raise HTTPException(**APP_MESSAGES["email_exists"])
#         elif user_created == "US0005":  # Si el dni no es válido
#             raise HTTPException(**APP_MESSAGES["invalid_dni"])

#         role = "Admin"
#         if user_created.id_rol == 2:
#             role = "Client"
#         elif user_created.id_rol == 3:
#             role = "Coach"

#         # Crear el token de acceso
#         access_token_expires = timedelta(
#             minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
#         access_token = create_access_token(
#             data={
#                 "email": user_created.email,
#                 "role": role,
#                 "id_usuario": user_created.id_usuario,
#                 "nombre": user_created.nombre,
#             },
#             expires_delta=access_token_expires,
#         )

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(e)
#         return Response(
#             ResponseSchema(
#                 detail=APP_MESSAGES["unexpected_error"]["detail"]
#             ).model_dump_json(),
#             status_code=APP_MESSAGES["unexpected_error"]["status_code"],
#             media_type="application/json",
#         )
#     else:
#         return Response(
#             ResponseSchema(
#                 detail=APP_MESSAGES["successfully_created"]["detail"],
#                 result=access_token,
#             ).model_dump_json(),
#             status_code=APP_MESSAGES["successfully_created"]["status_code"],
#             media_type="application/json",
#         )
