from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "TotalSell"
    environment: Literal["development", "test", "production"] = "development"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg://totalsell:totalsell@db:5432/totalsell"

    jwt_secret_key: str = Field(default="change-this-development-secret", min_length=16)
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 480
    refresh_token_days: int = 30

    admin_email: str = "admin@example.com"
    admin_password: str = Field(default="ChangeMe123!", min_length=8)

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @computed_field
    @property
    def cors_origin_list(self) -> list[str | AnyHttpUrl]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

