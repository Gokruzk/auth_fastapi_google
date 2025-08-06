from contextlib import asynccontextmanager
import os
import uvicorn
from colorama import Fore, Style
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import test_db_connection

from routers.auth import user 
#, auth

PORT = int(os.getenv("PORT"))
ENVIRONMENT = os.getenv("ENVIRONMENT")


def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            test_db_connection()
            print(
                f"\n{Fore.GREEN}{Style.BRIGHT}🚀 SLICKPATCH APP Server started on port {PORT}\n"
            )
            yield
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error: {str(e)}\n")
        finally:
            print(
                f"\n{Fore.YELLOW}{Style.BRIGHT}🛑 SLICKPATCH APP Server Shutdown\n")

    # Configuración condicional para documentación
    docs_url = "/docs" if ENVIRONMENT == "development" else None
    redoc_url = "/redoc" if ENVIRONMENT == "development" else None
    openapi_url = "/api/openapi.json" if ENVIRONMENT == "development" else None

    app = FastAPI(
        title="SLITCHPATCH APP API",
        description="",
        version="0.0.1",
        lifespan=lifespan,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()

# ==================== AUTENTICACIÓN Y USUARIOS ====================
# app.include_router(auth.router, prefix="/api/v1/auth",
#                    tags=["Autenticación"])

app.include_router(user.router, prefix="/api/v1/users", tags=["Usuarios"])

# ==================== ENDPOINTS DE UTILIDAD ====================
@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del sistema"""
    return {
        "status": "healthy",
        "service": "slickpatch_backend",
        "version": "0.0.1",
    }


@app.get("/")
async def root():
    """Endpoint raíz con información del API"""
    return {
        "message": "SLITCHPATCH APP API",
        "version": "0.0.1",
        "docs": (
            "/docs" if ENVIRONMENT == "development" else "Not available in production"
        ),
        "health": "/health",
    }


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", host="0.0.0.0", port=PORT, reload=True, timeout_keep_alive=300
    )
