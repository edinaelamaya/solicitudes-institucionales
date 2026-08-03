from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Prueba Tecnica Backend"
    app_version: str = "0.1.0"
    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/solicitudes"
    db_echo: bool = False
    consumer_base_url: str = "http://consumer:8001"
    request_timeout_seconds: float = 5.0
    max_retry_attempts: int = 3
    backend_log_file_path: str = "/logs/backend.jsonl"


@lru_cache
def get_settings() -> Settings:
    return Settings()
