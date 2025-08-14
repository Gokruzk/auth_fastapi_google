from abc import ABC, abstractmethod
from fastapi import HTTPException
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from config.config import ServerConfig


class AuthService(ABC):
    @abstractmethod
    def autenticar(self, authorization_response: str):
        pass


class GoogleAuthService(AuthService):

    def autenticar(self, authorization_response: str):
        return self.get_google_user_info(authorization_response)

    def clients_secrets_file(self) -> Flow:
        flow = Flow.from_client_secrets_file(
            "auth/client_secrets.json",
            scopes=[
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'
            ],
            redirect_uri=f"{ServerConfig.REDIRECT_URI()}/api/v1/auth/callback"
        )
        return flow

    def get_google_user_info(self, authorization_response: str):
        flow = self.clients_secrets_file()
        try:
            # Intercambia el código por tokens
            flow.fetch_token(authorization_response=authorization_response)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error fetching token: {e}")

        credentials = flow.credentials
        oauth2_client = build('oauth2', 'v2', credentials=credentials)

        return oauth2_client.userinfo().get().execute()
