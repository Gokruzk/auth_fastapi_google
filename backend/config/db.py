from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from colorama import Fore, Style

from config.config import DBConfig

# DB URL
SQLALCHEMY_DATABASE_URL = (
    f"{DBConfig.db_dialect()}://{DBConfig.db_user()}:{DBConfig.db_psw()}@"
    f"{DBConfig.db_host()}:{DBConfig.db_port()}/{DBConfig.db_name()}"
)

# create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True
)

# Create async session
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def test_db_connection():
    """
    Realiza un select simple a la DB para comprobar la conexión.
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            print(
                f"\n{Fore.GREEN}INFO:{Style.RESET_ALL} "
                f"    Test DB connection successfully\n"
            )
    except Exception as e:
        print(
            f"\n{Fore.RED}ERROR:{Style.RESET_ALL} "
            f"Test DB connection failed: {e}\n"
        )
    finally:
        await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Devuelve una sesión async de SQLAlchemy para inyectar en endpoints.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
