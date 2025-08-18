from fastapi import Query
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, HTMLResponse
import urllib.parse
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_session, ServerConfig
from auth.dtos import UsuarioDTO, Token
from auth.services import GoogleAuthService, UserService
from auth.utils import PasswordManager, ResponsesManager,TokenManager

router = APIRouter()


@router.post(
    path="/login",
    response_model=Token,
)
async def auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
):
    """
    Auth a user.

    :param form_data: User's credentials.
    :type form_data: dict[str, Any] with keys {"username": str, "password": str}
    :return: A dictionary with an access token and token type.
    :rtype: dict[str, Any] with keys {"access_token": str, "token_type": str}
    """
    service = UserService(db)
    user_data: UsuarioDTO = await service.find_by_email(email=form_data.username)
    
    if user_data == []:  # if the user does not exist
        return ResponsesManager.error("user_not_found")

    # Verificar la contraseña
    if not PasswordManager.verify_password(form_data.password, user_data.contrasena):
        return ResponsesManager.error("incorrect_email_psw")

    # Crear el token de acceso
    access_token = TokenManager.create_access_token(
        data={
            "email": user_data.email,
            "role": user_data.rol.rol,
            "nombre": user_data.nombres,
        }
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/login/google")
def login_google():
    """
    Auth a user by google.

    :redirect: A url to auth.
    """
    auth_service = GoogleAuthService()
    authorization_url, state = auth_service.clients_secrets_file().authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get("/callback")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_session)):
    """
    Create token with user info from Google.

    :param request: Request from /login/google
    :type request: Request
    :redirect: A web page to pass the token
    """
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
    """
    Send token to frontend.

    :param token: Request from /callback
    :type token: str
    """
    return f"""
    <html>
      <body>
        <script>
          const FRONTEND_ORIGIN = "http://localhost:3000";
          window.opener.postMessage({{ token: "{token}" }}, FRONTEND_ORIGIN);
          window.close();
        </script>
        <p>Autenticando...</p>
      </body>
    </html>
    """
