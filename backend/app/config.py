import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Academic Peer Review Simulator"
    database_url: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    frontend_origin: str = "http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if os.getenv("VERCEL"):
            return "sqlite:////tmp/peer_review.db"
        return self.database_url or "sqlite:///./peer_review.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()
