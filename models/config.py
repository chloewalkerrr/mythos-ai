from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    db_user: str
    db_name: str
    db_password: str = ""
    db_host: str = "localhost"
    db_port: str = "3306"


settings = Settings()
