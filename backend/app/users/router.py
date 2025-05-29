from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_db, get_current_user
from backend.app.users.schemas import UserCreate, UserRead, Token, LoginCredentials
from backend.app.users import crud
from backend.app.core.security import verify_password, create_access_token, create_refresh_token
from backend.app.users.models import User as UserModel # Renamed to avoid conflict with User schema


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user_by_username = crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    created_user = crud.create_user(db=db, user=user)
    return created_user

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: LoginCredentials, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    # current_user is a UserModel instance from get_current_user
    # Pydantic will convert it to UserRead for the response
    return current_user
