from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel # BaseModel might be needed if we were defining TokenData here
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.core.config import settings
from app.users.models import User
from app.users.crud import get_user_by_username # Assuming this function exists and takes (db, username)
from app.users.schemas import TokenData # Importing from schemas.py

# OAuth2PasswordBearer configuration
# The tokenUrl should match the actual login endpoint path
# From main.py: app.include_router(auth_router, prefix="/api/v1")
# From users/router.py: router = APIRouter(prefix="/auth", tags=["authentication"])
# So, full path is /api/v1/auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db():
    """
    FastAPI dependency to provide a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency to get the current user from a JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            # According to JWT spec, "sub" (subject) is the standard claim for principal identifier
            raise credentials_exception
        # TokenData validation can be implicitly handled by checking username presence
        # token_data = TokenData(username=username) # Not strictly necessary if only username is used from payload
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    FastAPI dependency to get the current active user.
    Relies on get_current_user and then checks the is_active flag.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
