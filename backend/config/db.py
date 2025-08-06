from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from colorama import Fore, Style

import os

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_DIALECT = os.getenv("DB_DIALECT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
SQLALCHEMY_DATABASE_URL = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@[{DB_HOST}]:5432/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def test_db_connection():
    try:
        # Intenta crear una sesión
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
