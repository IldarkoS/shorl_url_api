import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
CERTS_DIR = BASE_DIR / "src" / "users" / "auth" / "certs"

class AuthJWT(BaseModel):
    PRIVATE_KEY_PATH: Path = CERTS_DIR / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = CERTS_DIR / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30


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

    DB: DbSettings = DbSettings()

    AUTH_JWT: AuthJWT = AuthJWT()

    # class Config:
    #     env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()
