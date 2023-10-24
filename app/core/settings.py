from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_version: str
    app_v1_prefix: str
    debug: bool
    project_name: str
    project_description: str
    database_url: str
    mongodb_uri: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()

