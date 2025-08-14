from os import getenv
from dotenv import load_dotenv

load_dotenv()


class ServerConfig:
    @staticmethod
    def PORT() -> int | None:
        return int(getenv("PORT"))

    @staticmethod
    def ENVIRONMENT() -> str | None:
        return getenv("ENVIRONMENT")
    
    @staticmethod
    def REDIRECT_URI() -> str | None:
        return getenv("REDIRECT_URI")


class DBConfig():
    @staticmethod
    def DB_NAME() -> str | None:
        return getenv("DB_NAME")

    def DB_HOST() -> str | None:
        return getenv("DB_HOST")
    
    def DB_PORT() -> str | None:
        return getenv("DB_PORT")

    def DB_DIALECT() -> str | None:
        return getenv("DB_DIALECT")

    def DB_PASSWORD() -> str | None:
        return getenv("DB_PASSWORD")

    def DB_USER() -> str | None:
        return getenv("DB_USER")


class JWTConfig():
    def ALGORITHM() -> str | None:
        return getenv("ALGORITHM")

    def SECRET_KEY() -> str | None:
        return getenv("SECRET_KEY")

    def ACCESS_TOKEN_EXPIRE_MINUTES() -> int | None:
        return int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
