from sqlalchemy import Column, String, Boolean, Integer, DateTime # Integer might not be needed if id is from TimestampedModel

# Import TimestampedModel from base_model.py
# from backend.app.db.base_model import TimestampedModel
# Import Base if TimestampedModel is not used or if there's an issue
# from backend.app.db.database import Base

# Attempt to import TimestampedModel, fallback to Base if necessary
ParentModel = None
timestamp_model_fields_present = False
try:
    from app.db.base_model import TimestampedModel # Assuming 'app' is a package
    ParentModel = TimestampedModel
    timestamp_model_fields_present = True # Assume TimestampedModel provides id, created_at, updated_at
    print("Successfully imported TimestampedModel in users/models.py.")
except ImportError:
    print("Warning: Could not import TimestampedModel from app.db.base_model in users/models.py. Falling back to Base.")
    from app.db.database import Base # Assuming 'app' is a package - Fallback import
    ParentModel = Base
    # Explicitly define id, created_at, updated_at if not using TimestampedModel
    from sqlalchemy.sql import func
    # DateTime already imported at the top


class User(ParentModel):
    __tablename__ = "users"

    # Define common fields
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False) # Consider EmailType from sqlalchemy_utils if available
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False) # Made nullable=False for consistency

    # Email verification fields
    is_verified_email = Column(Boolean, default=False, nullable=False)
    email_verification_token = Column(String, nullable=True, index=True, unique=True)

    # Password reset fields
    password_reset_token = Column(String, nullable=True, index=True, unique=True)
    password_reset_token_expiry = Column(DateTime, nullable=True)

    # Add id, created_at, updated_at if not inherited from TimestampedModel
    if not timestamp_model_fields_present:
        print("User model: Adding id, created_at, updated_at fields as TimestampedModel was not used/imported correctly.")
        id = Column(Integer, primary_key=True, index=True)
        created_at = Column(DateTime, default=func.now())
        updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    elif ParentModel is None: # Should not happen with the logic above, but as a failsafe
        raise RuntimeError("ParentModel is None, cannot define User model.")


    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
