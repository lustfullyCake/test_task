from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str = "secrets"
    db_url: str = "postgresql://test:test@db:5432/test"
    secret_key: str = "MT5nvmFISm3k_NUKJtvSUEUH4R8HmdBSnXAnhvnJOjI="

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache(maxsize=32)
def get_settings() -> Settings:
    """
    Return settings
    :return:
    """
    return Settings()
