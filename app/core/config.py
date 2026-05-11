# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "CRM "

    DEBUG: bool = True

    # PostgreSQL
    DATABASE_URL: str = (
        "mysql+aiomysql://root:Vishnu2002@localhost:3306/crm_db"
    )

    # JWT
    SECRET_KEY: str = "your-secret-key"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()