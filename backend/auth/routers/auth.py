from fastapi import Query
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, HTMLResponse
import urllib.parse
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_session, ServerConfig
from auth.dtos import UsuarioDTO, Token
from auth.services import GoogleAuthService, UserService
from auth.utils import APP_MESSAGES, PasswordManager, TokenManager

router = APIRouter()


@router.post(
    path="/login",
    response_model=Token,
)
async def auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
):
    service = UserService(db)
    user_data: UsuarioDTO = await service.find_by_email(email=form_data.username)
    # Determinar el objeto del usuario autenticado
    authenticated_user = None

    if user_data:  # Si user_data no es vacío
        authenticated_user: UsuarioDTO = user_data

    # Si no se encuentra el usuario
    if not authenticated_user:
        raise HTTPException(
            status_code=APP_MESSAGES["user_not_found"]["status_code"],
            detail=APP_MESSAGES["user_not_found"]["detail"],
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar la contraseña
    if not PasswordManager.verify_password(form_data.password, authenticated_user.contrasena):
        raise HTTPException(
            status_code=APP_MESSAGES["incorrect_email_psw"]["status_code"],
            detail=APP_MESSAGES["incorrect_email_psw"]["detail"],
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear el token de acceso
    access_token = TokenManager.create_access_token(
        data={
            "email": authenticated_user.email,
            "role": user_data.rol.rol,
            "nombre": user_data.nombres,
        }
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/login/google")
def login_google():
    auth_service = GoogleAuthService()
    authorization_url, state = auth_service.clients_secrets_file().authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get("/callback")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_session)):

    # Autenticar con google
    service = GoogleAuthService()
    user_info = service.autenticar(str(request.url))

    # Crear el token de acceso
    access_token = TokenManager.create_access_token(
        data={
            "email": user_info["email"],
            "role": "User",
            "nombre": user_info["name"],
        }
    )

    token_encoded = urllib.parse.quote(access_token)

    # Redirige a página que tiene el script para enviar token al frontend
    redirect_url = f"{ServerConfig.redirect_uri()}/api/v1/auth/callback/success/?token={token_encoded}"

    return RedirectResponse(redirect_url)


@router.get("/callback/success", response_class=HTMLResponse)
async def auth_success(token: str = Query(...)):
    return f"""
    <html>
      <body>
        <script>
          // Origen de tu frontend
          const FRONTEND_ORIGIN = "http://localhost:3000";
          window.opener.postMessage({{ token: "{token}" }}, FRONTEND_ORIGIN);
          window.close();
        </script>
        <p>Autenticando...</p>
      </body>
    </html>
    """
