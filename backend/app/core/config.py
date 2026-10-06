from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # === LLM (elegí uno) ===
    # "openrouter" (gratis, sin tarjeta) | "gemini" (gratis) | "claude" (pago)
    llm_provider: str = "openrouter"
    openrouter_api_key: str = ""          # gratis: https://openrouter.ai/keys
    openrouter_model: str = "meta-llama/llama-3.3-70b-instruct:free"
    gemini_api_key: str = ""              # gratis: https://aistudio.google.com
    gemini_model: str = "gemini-2.5-flash-lite"
    anthropic_api_key: str = ""           # opcional

    # === APIs gratuitas de repositorios (opcionales) ===
    core_api_key: str = ""                # https://core.ac.uk/services/api (gratis)

    # === Base de datos ===
    database_url: str = "sqlite:///./thesisforge.db"
    redis_url: str = "redis://localhost:6379/0"

    # === Config ===
    cors_origins: str = "http://localhost:3000"
    max_results_per_source: int = 5
    request_timeout: int = 15

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self):
        return [o.strip() for o in self.cors_origins.split(",")]

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
