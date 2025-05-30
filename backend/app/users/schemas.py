from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional # Optional was used in the original based on subtask report

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr # Using EmailStr for validation

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    # Add fields from User model that should be in the read schema
    is_verified_email: bool = False # Default to False if not always present or to match model
    # email_verification_token: Optional[str] = None # Usually not exposed
    # password_reset_token: Optional[str] = None # Usually not exposed
    # password_reset_token_expiry: Optional[datetime] = None # Usually not exposed
    created_at: datetime
    updated_at: datetime

    # For Pydantic V2, use model_config. For V1, use class Config.
    # Assuming Pydantic V2 based on earlier setups.
    model_config = {
        "from_attributes": True  # Enables ORM mode / load from model attributes
    }
    # For Pydantic V1:
    # class Config:
    #     orm_mode = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str # Added refresh_token as per original plan
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None # Or user_id: Optional[int] = None

# Login Schemas
class LoginCredentials(BaseModel):
    username: str
    password: str

# Password Reset and Email Verification Schemas
class RequestPasswordResetSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str

class RequestEmailVerificationSchema(BaseModel):
    email: EmailStr # Or identify user by ID if they are logged in but unverified

class MessageSchema(BaseModel): # Generic message response
    message: str
