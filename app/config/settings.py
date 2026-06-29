from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ecommerce API"
    app_version: str = "0.1.0"
    app_description: str = "API de ecommerce - Proyecto FEM"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="APP_"
    )


settings = Settings()