from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # WhatsApp Cloud API
    whatsapp_token: str | None = None
    whatsapp_phone_id: str | None = None

    # Webhook verify token (Meta)
    verify_token: str

    # LLM (opcional)
    claude_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()