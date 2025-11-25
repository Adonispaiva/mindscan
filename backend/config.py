from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "MindScan Backend"
    VERSION: str = "2.0"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "mindscan"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "mindscan_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> "Settings":
    return Settings()