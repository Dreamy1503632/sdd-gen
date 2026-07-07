"""
config.py – centralised settings loaded from environment / .env
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── API keys ──────────────────────────────────────────────
    anthropic_api_key: str = ""
    openai_api_key: str = ""          # optional fallback

    # ── LLM config ───────────────────────────────────────────
    llm_provider: str = "anthropic"   # "anthropic" | "openai"
    llm_model: str = "claude-sonnet-4-20250514"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 8192

    # ── App config ────────────────────────────────────────────
    app_name: str = "Oracle Fusion HCM Solution Architect API"
    api_version: str = "v1"
    debug: bool = False

    # ── File storage ──────────────────────────────────────────
    temp_dir: str = "temp"            # uploaded files land here
    output_dir: str = "outputs"       # generated files written here

    # ── Redis (session/cache) ─────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"
    session_ttl_seconds: int = 86400  # 24 h

    # ── CORS ──────────────────────────────────────────────────
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()