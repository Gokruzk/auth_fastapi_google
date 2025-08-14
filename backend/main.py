from contextlib import asynccontextmanager
import os
import uvicorn
from colorama import Fore, Style
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from config.db import test_db_connection
from config.config import ServerConfig

from auth.routers import user, auth


def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            test_db_connection()
            print(
                f"\n{Fore.GREEN}{Style.BRIGHT}🚀Server started on port {ServerConfig.port()}\n"
            )
            yield
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error: {str(e)}\n")
        finally:
            print(
                f"\n{Fore.YELLOW}{Style.BRIGHT}🛑Server Shutdown\n")

    # Configuración condicional para documentación
    docs_url = "/docs" if ServerConfig.environment() == "development" else None
    redoc_url = "/redoc" if ServerConfig.environment() == "development" else None
    openapi_url = "/api/openapi.json" if ServerConfig.environment() == "development" else None

    app = FastAPI(
        title="API",
        description="",
        version="0.0.1",
        lifespan=lifespan,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000/", "*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()

# Esquema oauth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ==================== AUTENTICACIÓN Y USUARIOS ====================
app.include_router(auth.router, prefix="/api/v1/auth",
                   tags=["Autenticación"])

app.include_router(user.router, prefix="/api/v1/users", tags=["Usuarios"])

# ==================== ENDPOINTS DE UTILIDAD ====================


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del sistema"""
    return {
        "status": "healthy",
        "service": "backend",
        "version": "0.0.1",
    }


@app.get("/")
async def root():
    """Endpoint raíz con información del API"""
    return {
        "message": "API",
        "version": "0.0.1",
        "docs": (
            "/docs" if ServerConfig.environment() == "development" else "Not available in production"
        ),
        "health": "/health",
    }


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", host="0.0.0.0", port=ServerConfig.port(), reload=True, timeout_keep_alive=300
    )
