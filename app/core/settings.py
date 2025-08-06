from functools import lru_cache
from typing import Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nexus"
    environment: str = "dev"
    log_level: str = "INFO"
    redis_url: str = "redis://localhost:6379/0"

    # ⚡ Yeni — ajan → model haritası
    model_map: Dict[str, str] = {
        "planner": "openai-o3",
        "builder": "claude-4-sonnet",
        "tester": "gemini-2.5-pro",
    }

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> "Settings":
    return Settings()
