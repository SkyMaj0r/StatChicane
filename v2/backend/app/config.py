"""
app/config.py

Centralised configuration via pydantic-settings.
All values are read from environment variables (or from a .env file).
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    # Full SQLAlchemy connection URL, e.g.:
    #   mysql+mysqlconnector://user:password@localhost:3306/f1db
    DATABASE_URL: str

    # ------------------------------------------------------------------
    # Redis
    # ------------------------------------------------------------------
    # Connection URL for the Redis cache instance.
    REDIS_URL: str = "redis://localhost:6379"

    # ------------------------------------------------------------------
    # Google Gemini LLM
    # ------------------------------------------------------------------
    # API key obtained from Google AI Studio.
    GEMINI_API_KEY: str

    # Which Gemini model variant to use for NLP queries.
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # ------------------------------------------------------------------
    # JWT authentication
    # ------------------------------------------------------------------
    # A strong random secret used to sign JWT tokens.
    JWT_SECRET: str

    # Signing algorithm — HS256 is the standard symmetric choice.
    JWT_ALGORITHM: str = "HS256"

    # Number of minutes before an issued token expires.
    JWT_EXPIRY_MINUTES: int = 60

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    # Comma-separated list of allowed frontend origins.
    # Example: "http://localhost:3000,https://statchicanev2.com"
    CORS_ORIGINS: str = "http://localhost:3000"

    # ------------------------------------------------------------------
    # FastF1 telemetry cache
    # ------------------------------------------------------------------
    # Local directory where FastF1 caches telemetry data.
    FASTF1_CACHE_PATH: str = "./fastf1_cache"

    class Config:
        # Load variables from a .env file in the project root.
        env_file = ".env"
        env_file_encoding = "utf-8"


# Single shared settings instance — import this everywhere.
settings = Settings()
