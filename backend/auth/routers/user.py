from datetime import timedelta
from typing import List
from sqlalchemy.orm import Session
from config.db import get_db

from fastapi import APIRouter, Depends, HTTPException, Path, Response

from auth.dtos import UsuarioDTO, CreateUsuarioDTO, ResponseSchema, TokenData, Role
from auth.services import UserService
from auth.utils.managers import TokenManager, SessionManager
from auth.utils.messages import APP_MESSAGES

router = APIRouter()


@router.post(
    path="/all", response_model=ResponseSchema, response_model_exclude_none=True
)
async def get_all(
    # rol: int,
    token_data: TokenData = Depends(
        SessionManager.rol_checker([Role.admin.value, Role.user.value])),
    db: Session = Depends(get_db)
):
    try:
        service = UserService(db)
        # Obtener todos los usuarios
        data: List[UsuarioDTO] = await service.get_all()

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


@router.get(
    path="/{email}", response_model=ResponseSchema, response_model_exclude_none=True
)
async def find_by_email(
    email: str = Path(..., alias="email"),
    token_data: TokenData = Depends(
        SessionManager.rol_checker([Role.admin.value, Role.user.value])),
    db: Session = Depends(get_db)
):
    try:
        service = UserService(db)
        # Obtener usuario por email
        data: UsuarioDTO = await service.find_by_email(email)

        if data == "US9998":  # Mensaje de error
            raise HTTPException(**APP_MESSAGES["get_user_error"])
        elif data == []:  # Si no existe el usuario
            raise HTTPException(**APP_MESSAGES["user_not_found"])

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(
            ResponseSchema(
                detail=APP_MESSAGES["get_users_error"]["detail"]).model_dump_json(),
            status_code=APP_MESSAGES["get_users_error"]["status_code"],
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


@router.post(path="/admin", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(new_user: CreateUsuarioDTO, token_data: TokenData = Depends(SessionManager.rol_checker([Role.admin.value])), db: Session = Depends(get_db)):
    try:
        service = UserService(db)
        if new_user.id_rol == 3:
            user_created: UsuarioDTO = await service.create(new_user)
        else:
            pass
            # user_created: Usuario = await UserService.create_client(new_user)

        if user_created == "US9999":  # Mensaje de error
            raise HTTPException(**APP_MESSAGES["unexpected_error"])
        elif user_created == "US0002":  # Si el dni ya existe
            raise HTTPException(**APP_MESSAGES["dni_exists"])
        elif user_created == "US0003":  # Si el email ya existe
            raise HTTPException(**APP_MESSAGES["email_exists"])
        elif user_created == "US0004":  # Si el dni no es válido
            raise HTTPException(**APP_MESSAGES["invalid_dni"])

        role = "Admin"
        if user_created.id_rol == 3:
            role = "User"

        # Crear el token de acceso
        access_token = TokenManager.create_access_token(
            data={
                "email": user_created.email,
                "role": role,
                "nombre": user_created.nombres,
            },
        )

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
                detail=APP_MESSAGES["successfully_created"]["detail"],
                result=access_token,
            ).model_dump_json(),
            status_code=APP_MESSAGES["successfully_created"]["status_code"],
            media_type="application/json",
        )
