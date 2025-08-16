from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from colorama import Fore, Style

from config.config import DBConfig

SQLALCHEMY_DATABASE_URL = (
    f"{DBConfig.db_dialect()}://{DBConfig.db_user()}:{DBConfig.db_psw()}@"
    f"[{DBConfig.db_host()}]:{DBConfig.db_port()}/{DBConfig.db_name()}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)

# Fábrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def test_db_connection():
    """
    Hace un select a la base de datos para comprobar su estado
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            # `result.scalar()` devuelve el valor 1
            print(
                f"\n{Fore.GREEN}INFO:{Style.RESET_ALL}     "
                f"Test DB connection successfully\n"
            )

    except Exception as e:
        print(
            f"\n{Fore.RED}ERROR:{Style.RESET_ALL}    Test DB connection failed: {e}\n"
        )
    finally:
        await engine.dispose()


# Dependencia para FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
