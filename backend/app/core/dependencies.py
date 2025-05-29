from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session # Should be imported for type hint in get_current_user
from typing import Optional, Any # Ensure Optional and Any are imported

# --- get_db Implementation ---
try:
    from backend.app.db.database import SessionLocal
    print("Successfully imported SessionLocal in dependencies.py.")
except ImportError:
    print("Critical Error: Could not import SessionLocal from backend.app.db.database in dependencies.py")
    # Placeholder if SessionLocal cannot be imported
    class FakeSessionLocal:
        def __call__(self):
            print("Error: Using FakeSessionLocal - DB session will not work.")
            class FakeDb:
                def close(self): pass
            return FakeDb()
    SessionLocal = FakeSessionLocal # type: ignore

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- get_current_user Implementation ---

# Attempt to import necessary components
# Fallbacks are for ensuring subtask can run if environment is broken
decode_token_imported = False
users_crud_imported = False
users_models_imported = False
users_schemas_imported = False

try:
    from backend.app.core.security import decode_token
    decode_token_imported = True # Set flag for successful import
    from backend.app.users import crud as users_crud # Renamed to avoid conflict
    users_crud_imported = True
    from backend.app.users import models as users_models # Renamed
    users_models_imported = True
    from backend.app.users import schemas as users_schemas # Renamed
    users_schemas_imported = True
    print("Successfully imported dependencies for get_current_user in dependencies.py.")
except ImportError as e:
    print(f"Critical Error during import in dependencies.py (get_current_user): {e}. Using placeholders.")
    # Define placeholders if any import fails
    if not decode_token_imported:
        def decode_token(token: str) -> Optional[dict]: print("Warning: using placeholder decode_token"); return None
    if not users_crud_imported:
        class FakeCrud:
            def get_user_by_username(self, db, username: str) -> Optional[Any]: print("Warning: using placeholder users_crud.get_user_by_username"); return None
        users_crud = FakeCrud() # type: ignore
    if not users_models_imported:
        class FakeModels:
            class User: pass # Placeholder User model
        users_models = FakeModels() # type: ignore
    if not users_schemas_imported:
        class FakeSchemas:
            class TokenData: # Placeholder TokenData schema
                def __init__(self, username: Optional[str] = None): self.username = username
        users_schemas = FakeSchemas() # type: ignore


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") # Adjust tokenUrl if API prefix is used e.g. /api/v1/auth/login

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Optional[users_models.User]: # Return type is the ORM model
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Ensure decode_token is usable (either real or placeholder)
    if 'decode_token' not in globals() or not callable(decode_token):
        print("Critical runtime error: decode_token is not available.")
        raise credentials_exception

    payload = decode_token(token)
    if payload is None: # Check if decode_token itself returned None
        raise credentials_exception
    
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    try:
        # Validate username with TokenData schema, even if it's a placeholder
        token_data = users_schemas.TokenData(username=username)
    except Exception: # Catch potential validation error if TokenData is a real Pydantic model
        raise credentials_exception

    if token_data.username is None: # Redundant if TokenData requires username, but safe
         raise credentials_exception

    # Ensure users_crud is usable
    if 'users_crud' not in globals() or not hasattr(users_crud, 'get_user_by_username'):
        print("Critical runtime error: users_crud.get_user_by_username is not available.")
        raise credentials_exception
        
    user = users_crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user # Return the ORM model instance
