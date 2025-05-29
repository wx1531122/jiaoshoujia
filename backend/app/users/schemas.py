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
