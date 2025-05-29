from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

# Attempt to import actual settings, fallback to placeholder
settings_to_use = None
try:
    from backend.app.core.config import settings
    settings_to_use = settings
    print("Successfully imported actual settings in security.py.")
except ImportError as e:
    print(f"Warning: Could not import actual settings in security.py ({e}). Using placeholders.")
    class SettingsPlaceholder:
        JWT_SECRET_KEY: str = "fallback_secret_key_if_import_fails"
        JWT_ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    settings_to_use = SettingsPlaceholder()


# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Token Management
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings_to_use.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings_to_use.JWT_SECRET_KEY, algorithm=settings_to_use.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings_to_use.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    # Add a specific claim for refresh tokens if desired, e.g. "type": "refresh"
    # to_encode.update({"type": "refresh"}) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings_to_use.JWT_SECRET_KEY, algorithm=settings_to_use.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings_to_use.JWT_SECRET_KEY, algorithms=[settings_to_use.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
