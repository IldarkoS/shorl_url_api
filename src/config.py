import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

class AuthJWT(BaseModel):
    SECRET_KEY: str = "SUPER_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15


class DbSettings(BaseModel):
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "user"
    PASS: str = "password"
    NAME: str = "urls"
    ECHO: bool = False

    @property
    def URL(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"


class Settings(BaseSettings):

    DAYS_UNTIL_EXPIRED: int = 1
    SHORT_URL_LENGHT: int = 6
    MAX_GENERATION_ATTEMPTS: int = 3
    ALPHABET: str = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789" # Exclude O0Il1
    BASE_URL: str = "http://localhost:8000"

    DB: DbSettings = DbSettings()

    AUTH_JWT: AuthJWT = AuthJWT()

    # class Config:
    #     env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()
