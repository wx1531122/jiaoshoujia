from pydantic_settings import BaseSettings # Keep for potential future Pydantic V2 features
import os
from dotenv import load_dotenv
from typing import Union # For bool conversion

# Explicitly load from backend/.env
# The path to .env is calculated from this file's location (backend/app/core/config.py)
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, override=True)

# Helper function to convert string to bool for env vars
def _str_to_bool(val: Union[str, bool]) -> bool:
    if isinstance(val, bool):
        return val
    return val.lower() in ('true', '1', 't', 'yes', 'y')

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:default_password@host:5432/default_db")
    
    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", str(60 * 24 * 7)))

    # Email settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "your_mail_username")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "your_mail_password")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "your_mail_from_email@example.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "your_mail_server")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Your Application Name")
    MAIL_STARTTLS: bool = _str_to_bool(os.getenv("MAIL_STARTTLS", "True"))
    MAIL_SSL_TLS: bool = _str_to_bool(os.getenv("MAIL_SSL_TLS", "False"))
    USE_CREDENTIALS: bool = _str_to_bool(os.getenv("USE_CREDENTIALS", "True"))
    VALIDATE_CERTS: bool = _str_to_bool(os.getenv("VALIDATE_CERTS", "True"))
    MAIL_CONSOLE_OUTPUT: bool = _str_to_bool(os.getenv("MAIL_CONSOLE_OUTPUT", "False"))


    # If you were using Pydantic V2's SettingsConfigDict for .env loading:
    # model_config = SettingsConfigDict(
    #     env_file=dotenv_path,
    #     env_file_encoding='utf-8',
    #     extra='ignore'
    # )

settings = Settings()

# Debug print for DATABASE_URL (can be removed or expanded for other settings if needed)
print(f"DEBUG [config.py]: Loaded DATABASE_URL = {settings.DATABASE_URL}")
# print(f"DEBUG [config.py]: MAIL_CONSOLE_OUTPUT = {settings.MAIL_CONSOLE_OUTPUT}")
# print(f"DEBUG [config.py]: MAIL_PORT = {settings.MAIL_PORT} (type: {type(settings.MAIL_PORT)})")
# print(f"DEBUG [config.py]: MAIL_STARTTLS = {settings.MAIL_STARTTLS} (type: {type(settings.MAIL_STARTTLS)})")
