from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    db_user: str
    db_name: str
    db_password: SecretStr = ""
    db_host: str = "localhost"
    db_port: str = "3306"
    lm_studio_base_url: str = "http://127.0.0.1:1234"
    lm_studio_model: str = "qwen/qwen3-4b-2507"
    lm_studio_timeout_seconds: float = 120.0


settings = Settings()
