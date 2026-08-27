from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ResolveAI"
    environment: str = "development"
    debug: bool = True

    database_url: str = "postgresql://resolveai:resolveai_secret@localhost:5432/resolveai_db"
    primary_llm_provider: str = "gemini"
    gemini_api_key: str | None = None
    openrouter_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
