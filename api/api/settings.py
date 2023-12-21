"""Settings for the API."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the API."""

    QDRANT_URL: str
    QDRANT_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

__all__ = ["settings"]
