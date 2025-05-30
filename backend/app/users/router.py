from typing import Any, Optional 
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks # Added BackgroundTasks
from sqlalchemy.orm import Session

# Corrected imports using 'app.' prefix
from app.users import crud
from app.users import models
from app.users import schemas
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.core.dependencies import get_db, get_current_active_user, get_current_user # get_current_user might be needed for other endpoints

# New imports for email verification and password reset
from app.core.email_service import send_email_verification_email, send_password_reset_email
from app.core.exceptions import (
    UserNotFoundException, 
    EmailVerificationTokenInvalid, 
    PasswordResetTokenInvalid, 
    UserAlreadyVerifiedException,
    EmailAlreadyExistsException, # For register endpoint
    UsernameAlreadyExistsException # For register endpoint
)


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks() # Added for sending verification email
):
    db_user_by_username = crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise UsernameAlreadyExistsException() # Using custom exception

    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise EmailAlreadyExistsException() # Using custom exception
    
    created_user = crud.create_user(db=db, user=user)
    
    # Set verification token and send email
    token_user = crud.set_email_verification_token(db, user=created_user)
    if not token_user.email_verification_token:
        # This case should ideally not happen if token generation is robust
        # Log an error here
        print(f"Error: Could not generate verification token for user {token_user.id}")
        # Optionally, raise an HTTPException if this is critical, 
        # or proceed without verification if system allows (not recommended)
    else:
        background_tasks.add_task(
            send_email_verification_email,
            recipient_email=token_user.email,
            username=token_user.username,
            token=token_user.email_verification_token
        )
    return created_user


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.LoginCredentials, db: Session = Depends(get_db)):
    user_obj = crud.get_user_by_username(db, username=form_data.username)
    
    if not user_obj or not verify_password(form_data.password, user_obj.hashed_password):
        raise HTTPException( # Keeping standard HTTPException for login failure
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user_obj.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user") # Standard HTTPException
    
    access_token = create_access_token(data={"sub": user_obj.username})
    refresh_token = create_refresh_token(data={"sub": user_obj.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead) # Optional removed from response_model as it should always return user or raise error
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

# --- New Endpoints for Email Verification and Password Reset ---

@router.post("/request-email-verification", response_model=schemas.MessageSchema, status_code=status.HTTP_200_OK)
async def request_email_verification(
    user_email_schema: schemas.RequestEmailVerificationSchema,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    user = crud.get_user_by_email(db, email=user_email_schema.email)
    if not user:
        # To prevent user enumeration, return a generic success message.
        # Log this event for monitoring if desired.
        return {"message": "If an account with this email exists and requires verification, a new link has been sent."}

    if user.is_verified_email:
        # Option 1: Inform user (might lead to enumeration if error is different)
        # raise UserAlreadyVerifiedException() 
        # Option 2: Silently re-send (as implemented here)
        # Option 3: Generic message like above
        pass # Allowing re-send for now

    updated_user = crud.set_email_verification_token(db, user=user)
    if not updated_user.email_verification_token:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate verification token.")

    background_tasks.add_task(
        send_email_verification_email,
        recipient_email=updated_user.email,
        username=updated_user.username,
        token=updated_user.email_verification_token
    )
    return {"message": "If your email is registered and requires verification, a new verification link has been sent."}


@router.get("/verify-email/{token}", response_model=schemas.MessageSchema, status_code=status.HTTP_200_OK)
async def verify_email(token: str, db: Session = Depends(get_db)):
    user = crud.verify_user_by_email_token(db, token=token)
    if not user:
        raise EmailVerificationTokenInvalid() # Custom exception
    return {"message": "Email verified successfully."}


@router.post("/request-password-reset", response_model=schemas.MessageSchema, status_code=status.HTTP_200_OK)
async def request_password_reset(
    request_data: schemas.RequestPasswordResetSchema,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    user = crud.get_user_by_email(db, email=request_data.email)
    if user: # Only proceed if user exists
        updated_user = crud.set_password_reset_token(db, user=user)
        if not updated_user.password_reset_token: # Should ideally not happen
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate password reset token.")

        background_tasks.add_task(
            send_password_reset_email,
            recipient_email=updated_user.email,
            username=updated_user.username,
            token=updated_user.password_reset_token
        )
    # Always return a generic message to prevent user enumeration
    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post("/reset-password", response_model=schemas.MessageSchema, status_code=status.HTTP_200_OK)
async def reset_password(
    request_data: schemas.ResetPasswordSchema, 
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_password_reset_token(db, token=request_data.token)
    if not user:
        # This handles expired or invalid tokens via get_user_by_password_reset_token's logic
        raise PasswordResetTokenInvalid() # Custom exception

    crud.reset_user_password(db, user=user, new_password=request_data.new_password)
    return {"message": "Password has been reset successfully."}
