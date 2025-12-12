from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # WhatsApp
    whatsapp_token: str
    whatsapp_phone_id: str
    verify_token: str

    # Claude / OpenAI (dejamos OpenAI opcional por si no lo usas)
    claude_api_key: str | None = None
    openai_api_key: str | None = None

    # DB
    database_url: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # <- clave para que no reviente si hay variables extra
    )

settings = Settings()