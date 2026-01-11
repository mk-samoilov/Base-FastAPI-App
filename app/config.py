"""
Application configuration.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application info
    app_title: str = "Base FastAPI App"
    app_description: str = "FastAPI application with plugin-based updates system"
    app_version: str = "0.1.0"

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    auto_reload: bool = True

    # Database settings
    database_url: str = "sqlite+aiosqlite:///database.db"

    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379

    # Logging
    log_level: str = "DEBUG"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
