from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@host:port/database"
    JWT_SECRET_KEY: str = "your-default-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    model_config = SettingsConfigDict(
        env_file="../../.env", # Relative path from backend/app/core/config.py to backend/.env
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
