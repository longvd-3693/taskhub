from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "TaskHub API"
    environment: str = "development"
    debug: bool = False

    database_url: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    redis_url: str
    task_cache_ttl: int = 300

    default_page_size: int = Field(default=20, ge=1)
    max_page_size: int = Field(default=100, ge=1)


def get_env_file() -> str:
    env = Path(".env").read_text() if Path(".env").exists() else ""

    for line in env.splitlines():
        if line.startswith("ENVIRONMENT="):
            environment = line.split("=", 1)[1].strip()
            return f".env.{environment}"

    return ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        _env_file=get_env_file(),
    )


settings = get_settings()
