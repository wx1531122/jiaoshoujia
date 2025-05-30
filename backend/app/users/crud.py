from sqlalchemy.orm import Session
from typing import Optional
import secrets
from datetime import datetime, timedelta, timezone # Ensure timezone for tz-aware datetimes

# Corrected imports using 'app.' prefix
from app.users import models
from app.users import schemas # Though not directly used in all new functions, good to keep if file grows
from app.core.security import get_password_hash

# Placeholder for token expiry settings (can be moved to config.py later if needed)
EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS = 48 # Not used if email_verification_token_expiry is omitted from model/logic
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = 1


# --- Existing CRUD functions (adjusted for corrected imports) ---

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User: # Return type changed to non-optional based on typical usage
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
        # is_active is True by default in model
        # is_verified_email is False by default in model
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- New functions for email verification and password reset ---

def generate_secure_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)

# --- Email Verification ---
def set_email_verification_token(db: Session, user: models.User) -> models.User:
    token = generate_secure_token()
    user.email_verification_token = token
    # user.email_verification_token_expiry = datetime.now(timezone.utc) + timedelta(hours=EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS) # Omitted as per instruction
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email_verification_token(db: Session, token: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email_verification_token == token).first()

def verify_user_by_email_token(db: Session, token: str) -> Optional[models.User]:
    user = get_user_by_email_verification_token(db, token)
    if user:
        # Optional: Check token expiry if implemented
        # if user.email_verification_token_expiry and user.email_verification_token_expiry < datetime.now(timezone.utc): # Omitted
        #     # Token expired, clear it or handle as needed
        #     user.email_verification_token = None
        #     # user.email_verification_token_expiry = None # Omitted
        #     db.commit()
        #     return None 
        user.is_verified_email = True
        user.email_verification_token = None # Clear token after use
        # user.email_verification_token_expiry = None # Omitted
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return None

# --- Password Reset ---
def set_password_reset_token(db: Session, user: models.User) -> models.User:
    token = generate_secure_token()
    user.password_reset_token = token
    user.password_reset_token_expiry = datetime.now(timezone.utc) + timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_password_reset_token(db: Session, token: str) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.password_reset_token == token).first()
    if user:
        if user.password_reset_token_expiry and user.password_reset_token_expiry < datetime.now(timezone.utc):
            # Token expired, clear it
            user.password_reset_token = None
            user.password_reset_token_expiry = None
            db.add(user) # Persist the clearing of the token
            db.commit()
            return None # Effectively, user not found with a valid token
        return user
    return None

def reset_user_password(db: Session, user: models.User, new_password: str) -> models.User:
    user.hashed_password = get_password_hash(new_password)
    user.password_reset_token = None # Clear token after use
    user.password_reset_token_expiry = None # Clear expiry
    # Optional: Force logout of other sessions if needed, e.g., by changing a security stamp field
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
