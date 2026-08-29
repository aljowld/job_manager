from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    database_url: str = Field(default="postgresql+psycopg://job_manager:job_manager@localhost:5432/job_manager", alias="DATABASE_URL")
    api_prefix: str = Field(default="/api/v1", alias="API_PREFIX")


settings = Settings()
