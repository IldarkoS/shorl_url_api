import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class AuthJWT(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", "../.env"),
        extra="ignore",
        env_prefix="AUTH_",
    )

    SECRET_KEY: str = "SUPER_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", "../.env"),
        extra="ignore",
        env_prefix="DB_",
    )

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
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", "../.env"),
        extra="ignore",
    )

    DAYS_UNTIL_EXPIRED: int = 1
    SHORT_URL_LENGHT: int = 5
    MAX_GENERATION_ATTEMPTS: int = 3
    ALPHABET: str = (
        "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"  # Exclude O0Il1
    )
    BASE_URL: str = "http://localhost:8000"

    DB: DbSettings = Field(default_factory=DbSettings)

    AUTH_JWT: AuthJWT = Field(default_factory=AuthJWT)


settings = Settings()
