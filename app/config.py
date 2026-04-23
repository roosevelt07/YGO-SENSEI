"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings sourced from a .env file or shell environment.

    Attributes:
        anthropic_api_key: Secret key for the Anthropic LLM service.
        llm_model: Claude model identifier used for deck analysis.
        ygoprodeck_base_url: Base URL for the YGOPRODeck card database API.
        http_timeout: Timeout in seconds applied to all outbound HTTP requests.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    anthropic_api_key: str
    llm_model: str = "claude-haiku-4-5-20251001"
    ygoprodeck_base_url: str = "https://db.ygoprodeck.com/api/v7"
    http_timeout: int = 10


settings = Settings()
