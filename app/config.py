"""Configuration — loads from .env."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8000
    host: str = "0.0.0.0"
    loglevel: str = "INFO"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    claude_api_key: str = ""
    deepseek_api_key: str = ""
    grok_api_key: str = ""
    openrouter_api_key: str = ""
    elevenlabs_api_key: str = ""
    ai_default_model: str = "gpt-4o"
    codewords_api_key: str = ""
    codewords_runtime_uri: str = ""
    whatsapp_auth_type: str = "qr"
    whatsapp_pairing_code: str = ""
    whatsapp_session_dir: str = "./.whatsapp_auth"
    whatsapp_phone_number_id: str = ""
    whatsapp_business_token: str = ""
    database_type: str = "sqlite"
    database_url: str = "sqlite:///astra.db"
    redis_url: str = "redis://localhost:6379"
    postgres_url: str = ""
    mysql_url: str = ""
    mongodb_url: str = ""
    github_pat: str = ""
    jwt_secret: str = "change-me"
    admin_username: str = "admin"
    admin_password: str = "admin123"
    api_key_header: str = "X-API-Key"
    api_keys: str = ""
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 30
    dashboard_enabled: bool = True
    dashboard_username: str = "admin"
    dashboard_password: str = "admin123"
    webhook_verify_token: str = "astra-webhook-token"
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
