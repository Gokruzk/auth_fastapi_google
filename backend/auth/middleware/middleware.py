import asyncio
from abc import ABC, abstractmethod
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from auth.utils import TokenManager
from auth.services import LogService
from config import AsyncSessionLocal


class CustomMiddleware(BaseHTTPMiddleware, ABC):
    @abstractmethod
    async def dispatch(self, request: Request, call_next) -> Response:
        pass


async def save_log_task(log_data):
    try:
        async with AsyncSessionLocal() as session:
            service = LogService(session)
            await service.register_log(log_data)
    except Exception as e:
        print("Error al guardar log:", e)


class LoggingMiddleware(CustomMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Determinar quién hizo la petición
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = TokenManager.decode_token(token)
            host = payload.get("email")
        else:
            host = f"{request.client.host}:{request.client.port}"

        # Datos del log
        log_data = {
            "quien": host,
            "accion": request.method,
            "entidad_afectada": request.url.path,
            "extra_data": response.status_code
        }

        # Crear tarea de fondo
        asyncio.create_task(save_log_task(log_data))

        return response
