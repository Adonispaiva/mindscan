from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SynMind API"
    OPENAI_API_KEY: str | None = None
    REDIS_URL: str = "redis://redis:6379/0"
    DATABASE_URL: str = "postgresql://mindscan:mindscan@db:5432/mindscan"

    class Config:
        env_file = ".env"

settings = Settings()
