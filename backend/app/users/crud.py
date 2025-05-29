from sqlalchemy.orm import Session
from typing import Optional # Added for type hints

# Attempt to import necessary local modules
# If worker has issues, it should note them. These imports are critical.
models_imported = False
schemas_imported = False
security_imported = False

try:
    from backend.app.users import models
    models_imported = True
    print("Successfully imported 'models' in crud.py.")
except ImportError as e:
    print(f"Critical Error during import of 'models' in crud.py: {e}. This will likely cause failures.")
    class FakeModelUser: pass # Placeholder for models.User
    class ModelsPlaceholder: User = FakeModelUser
    models = ModelsPlaceholder() # type: ignore

try:
    from backend.app.users import schemas
    schemas_imported = True
    print("Successfully imported 'schemas' in crud.py.")
except ImportError as e:
    print(f"Critical Error during import of 'schemas' in crud.py: {e}. This will likely cause failures.")
    class FakeSchemaUserCreate: pass # Placeholder for schemas.UserCreate
    class SchemasPlaceholder: UserCreate = FakeSchemaUserCreate
    schemas = SchemasPlaceholder() # type: ignore

try:
    from backend.app.core.security import get_password_hash
    security_imported = True
    print("Successfully imported 'get_password_hash' in crud.py.")
except ImportError as e:
    print(f"Critical Error during import of 'get_password_hash' in crud.py: {e}. This will likely cause failures.")
    def get_password_hash(p: str) -> str:
        print("Warning: Using fake_get_password_hash due to import error.")
        return "fake_hashed_password_for_" + p


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    if not models_imported:
        print("Warning: 'models.User' not available in get_user due to import error.")
        return None
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    if not models_imported:
        print("Warning: 'models.User' not available in get_user_by_username due to import error.")
        return None
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    if not models_imported:
        print("Warning: 'models.User' not available in get_user_by_email due to import error.")
        return None
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> Optional[models.User]:
    if not models_imported or not schemas_imported or not security_imported:
        print("Warning: Cannot create user due to import errors for models, schemas, or security.")
        return None # Or raise an exception
        
    hashed_password = get_password_hash(user.password)
    # Ensure user.username and user.email are accessed correctly based on UserCreate schema
    # For Pydantic models, direct attribute access user.username is correct.
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
