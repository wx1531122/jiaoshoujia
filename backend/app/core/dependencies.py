from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError # Ensure JWTError is imported for decode_token's potential exception
from backend.app.core.security import decode_token
from backend.app.core.config import settings
from backend.app.users import crud as users_crud # Aliased to avoid potential naming conflicts
from backend.app.users.models import User as UserModel # Aliased for clarity
from backend.app.users.schemas import TokenData
from backend.app.db.database import SessionLocal

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # Matches the login endpoint in users/router.py

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
        
    username: str | None = payload.get("sub")
    if username is None:
        raise credentials_exception
        
    # Validate payload with TokenData schema (optional but good practice)
    try:
        token_data = TokenData(username=username)
    except Exception: # Catch Pydantic validation error if username is not valid
        raise credentials_exception

    user = users_crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user
