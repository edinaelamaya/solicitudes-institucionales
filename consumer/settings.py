from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConsumerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    backend_base_url: str = "http://localhost:8000"
    request_timeout_seconds: float = 5.0
    max_retry_attempts: int = 3
    log_level: str = "INFO"
    consumer_log_file_path: str = "/logs/consumer.jsonl"


@lru_cache
def get_consumer_settings() -> ConsumerSettings:
    return ConsumerSettings()
