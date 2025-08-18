from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from config import get_session

from fastapi import APIRouter, Depends, Path
from auth.dtos import UsuarioDTO, CreateUsuarioDTO, ResponseSchema, TokenData, Role
from auth.services import UserService
from auth.utils import TokenManager, SessionManager, ResponsesManager

router = APIRouter()


@router.post(
    path="/all", response_model=ResponseSchema, response_model_exclude_none=True
)
async def get_all(
    # rol: int,
    token_data: TokenData = Depends(
        SessionManager.rol_checker([Role.admin.value, Role.user.value])),
    db: AsyncSession = Depends(get_session)
):
    """
    Gell all the users.

    :param rol: User's rol to search.
    :type rol: int
    :return: A dictionary with a detail message and the users data.
    :rtype: dict[str, Any] with keys {"detail": str, "result": List[UsuarioDTO]}
    """
    try:
        service = UserService(db)
        # Obtener todos los usuarios
        data: List[UsuarioDTO] = await service.get_all()

        if data == "US9998":  # Mensaje de error
            return ResponsesManager.error("get_users_error")
        elif data == []:  # Si no hay usuarios
            return ResponsesManager.error("no_users_found")

    except Exception as e:
        print(e)
        return ResponsesManager.error("unexpected_error")
    else:
        return ResponsesManager.success(data=data, message_key="successfully_retrieved")


@router.get(
    path="/{email}", response_model=ResponseSchema, response_model_exclude_none=True
)
async def find_by_email(
    email: str = Path(..., alias="email"),
    token_data: TokenData = Depends(
        SessionManager.rol_checker([Role.admin.value, Role.user.value])),
    db: AsyncSession = Depends(get_session)
):
    """
    Search a user by email.

    :param email: User's email address to search.
    :type email: str
    :return: A dictionary with a detail message and the user data.
    :rtype: dict[str, Any] with keys {"detail": str, "result": UsuarioDTO}
    """
    try:
        service = UserService(db)
        # Obtener usuario por email
        data: UsuarioDTO = await service.find_by_email(email)

        if data == "US9998":  # Mensaje de error
            return ResponsesManager.error("get_users_error")
        elif data == []:  # Si no existe el usuario
            return ResponsesManager.error("user_not_found")

    except Exception as e:
        print(e)
        return ResponsesManager.error("get_users_error")
    else:
        return ResponsesManager.success(data=data, message_key="successfully_retrieved")


@router.post(path="/admin", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(new_user: CreateUsuarioDTO, token_data: TokenData = Depends(SessionManager.rol_checker([Role.admin.value])), db: AsyncSession = Depends
                      (get_session)):
    """
    Create a user by an admin account

    :param new_user: User's info
    :type new_user: CreateUsuarioDTO
    :return: A dictionary with a detail message and the access token.
    :rtype: dict[str, Any] with keys {"detail": str, "result": str}
    """
    try:
        service = UserService(db)
        user_created: UsuarioDTO = await service.create(new_user)

        if user_created == "US9999":  # Mensaje de error
            return ResponsesManager.error("get_users_error")
        elif user_created == "US0002":  # Si el dni ya existe
            return ResponsesManager.error("dni_exists")
        elif user_created == "US0003":  # Si el email ya existe
            return ResponsesManager.error("email_exis")
        elif user_created == "US0004":  # Si el dni no es válido
            return ResponsesManager.error("invalid_dn")

        role = "Admin"
        if user_created.id_rol == 2:
            role = "User"

        # Crear el token de acceso
        access_token = TokenManager.create_access_token(
            data={
                "email": user_created.email,
                "role": role,
                "nombre": user_created.nombres,
            },
        )

    except Exception as e:
        print(e)
        return ResponsesManager.error("unexpected_error")
    else:
        return ResponsesManager.success(data=access_token, message_key="successfully_created")
