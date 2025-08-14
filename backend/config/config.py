from os import getenv
from dotenv import load_dotenv

load_dotenv()


class ServerConfig:
    @staticmethod
    def port() -> int | None:
        return int(getenv("PORT"))

    @staticmethod
    def environment() -> str | None:
        return getenv("ENVIRONMENT")

    @staticmethod
    def redirect_uri() -> str | None:
        return getenv("REDIRECT_URI")


class DBConfig():
    @staticmethod
    def db_name() -> str | None:
        return getenv("DB_NAME")

    def db_host() -> str | None:
        return getenv("DB_HOST")

    def db_port() -> str | None:
        return getenv("DB_PORT")

    def db_dialect() -> str | None:
        return getenv("DB_DIALECT")

    def db_psw() -> str | None:
        return getenv("DB_PASSWORD")

    def db_user() -> str | None:
        return getenv("DB_USER")


class JWTConfig():
    def alogrithm() -> str | None:
        return getenv("ALGORITHM")

    def secret_key() -> str | None:
        return getenv("SECRET_KEY")

    def token_expire() -> int | None:
        return int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
