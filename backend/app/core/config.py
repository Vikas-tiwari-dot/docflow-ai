from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "DocFlow AI"
    environment: str = "development"
    database_url: str = "sqlite:///./docflow.db"
    jwt_secret: str = "dev-only-change-me"
    jwt_expire_minutes: int = 60
    cors_origins: str = "http://localhost:5173"
    max_file_size_mb: int = 10
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str = "http://localhost:8000/api/integrations/google/callback"
    frontend_url: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings():
    return Settings()
