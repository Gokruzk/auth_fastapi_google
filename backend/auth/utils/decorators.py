from functools import wraps
from typing import Callable

from fastapi import HTTPException


def validate_data(func):
    """
    Decorador para validar datos de entrada
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Aquí se pueden agregar validaciones específicas
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=f"Datos inválidos: {str(e)}")

    return wrapper


def validate_date_logic(func):
    """
    Decorador para validar lógica de fechas en tracking
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            error_msg = str(e).lower()

            if "fecha" in error_msg:
                if "formato" in error_msg:
                    raise HTTPException(
                        status_code=400,
                        detail="Formato de fecha inválido. Use YYYY-MM-DD",
                    )
                elif "futura" in error_msg:
                    raise HTTPException(
                        status_code=400,
                        detail="No se pueden crear sesiones para fechas futuras",
                    )
                elif "pasada" in error_msg:
                    raise HTTPException(
                        status_code=400,
                        detail="No se pueden modificar sesiones de fechas pasadas",
                    )

            raise HTTPException(
                status_code=400, detail=f"Error de validación: {str(e)}"
            )

    return wrapper


def clean_response_fields(fields_to_clean: list[str]):
    """
    Decorador para limpiar campos específicos de forma recursiva en diccionarios y objetos anidados.
    """

    def clean(obj):
        if isinstance(obj, list):
            return [clean(item) for item in obj]

        elif isinstance(obj, dict):
            return {
                k: clean(v)
                for k, v in obj.items()
                if k not in fields_to_clean and v is not None
            }

        elif hasattr(obj, "__dict__"):
            for field in fields_to_clean:
                if hasattr(obj, field):
                    delattr(obj, field)
            # Aplicar limpieza recursiva también en los atributos
            for attr, value in vars(obj).items():
                setattr(obj, attr, clean(value))
            return obj

        return obj

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return clean(result)

        return wrapper

    return decorator


# Decorador para eliminar atributos nulos
def clean_fields(fields_to_clean: list[str]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)

            # Limpieza de datos en una lista de objetos
            if isinstance(result, list):
                for obj in result:
                    for field in fields_to_clean:
                        if hasattr(obj, field):
                            delattr(obj, field)

            # Limpieza de datos en un único objeto
            elif isinstance(result, object):
                for field in fields_to_clean:
                    if hasattr(result, field):
                        delattr(result, field)

            return result

        return wrapper

    return decorator


def handle_service_exceptions():
    """Decorador para manejar excepciones en servicios"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                raise  # Re-lanzar HTTPExceptions
            except Exception as e:
                print(f"Error en {func.__name__}: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Error interno en {func.__name__}"
                )

        return wrapper

    return decorator
