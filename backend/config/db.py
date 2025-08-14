from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from colorama import Fore, Style

from config.config import DBConfig

SQLALCHEMY_DATABASE_URL = f"{DBConfig.db_dialect()}://{DBConfig.db_user()}:{DBConfig.db_psw()}@[{DBConfig.db_host()}]:{DBConfig.db_port()}/{DBConfig.db_name()}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependencia para crear una sesión para cada operación
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def test_db_connection():
    """
    Hace un select a la base de datos para comprobar su estado
    """
    try:
        # Crea una sesión
        db = SessionLocal()
        # Ejecuta una consulta simple para probar la conexión
        db.execute(text("SELECT 1"))
        db.close()

        print(
            f"\n{Fore.GREEN}INFO:{Style.RESET_ALL}     Test DB connection successfully\n"
        )

    except Exception as e:
        print(
            f"\n{Fore.RED}ERROR:{Style.RESET_ALL}    Test DB connection failed: {e}\n"
        )
