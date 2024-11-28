from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_domain: str
    database_user: str
    database_password: str
    users_database_name: str
    data_database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# region settings
@lru_cache
def get_settings() -> Settings:
    return Settings()


# endregion
