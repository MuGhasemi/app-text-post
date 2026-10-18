from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Settings class to manage environment variables.
    Pydantic will automatically load variables from a .env file.
    """
    DB_CONNECTION: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    API_PREFIX: str
    APP_DEBUG: bool = False
    SECRET_KEY:str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False)


@lru_cache()
def get_settings() -> Settings:
    """Caches settings object to prevent redundant loading."""
    return Settings()  # type: ignore
