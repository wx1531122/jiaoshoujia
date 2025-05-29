from typing import Any, Optional 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Attempt to import local modules (crud, models, schemas, security) - Retain existing robust fallbacks
crud_imported = False
models_imported = False
schemas_imported = False
security_imported = False

try:
    from backend.app.users import crud
    crud_imported = True
    print("Successfully imported 'crud' in users/router.py.")
except ImportError as e:
    print(f"Critical Error during import of 'crud' in users/router.py: {e}.")
    class FakeCRUD:
        def get_user_by_username(self, db, username): return None
        def get_user_by_email(self, db, email): return None
        def create_user(self, db, user): return None
    crud = FakeCRUD() # type: ignore

try:
    from backend.app.users import models
    models_imported = True
    print("Successfully imported 'models' in users/router.py.")
except ImportError as e:
    print(f"Critical Error during import of 'models' in users/router.py: {e}.")
    class FakeModels: # Renamed from original prompt for clarity
        class User: # Placeholder User model
            # Add attributes if they are accessed by router logic before actual db interaction
            # e.g. username: Optional[str] = None; email: Optional[str] = None etc.
             pass 
    models = FakeModels() # type: ignore

try:
    from backend.app.users import schemas
    schemas_imported = True
    print("Successfully imported 'schemas' in users/router.py.")
except ImportError as e:
    print(f"Critical Error during import of 'schemas' in users/router.py: {e}.")
    class FakeSchemas: # Renamed from original prompt
        class UserCreate: pass
        class UserRead: pass
        class Token: pass
        class LoginCredentials: pass
    schemas = FakeSchemas() # type: ignore

try:
    from backend.app.core.security import create_access_token, create_refresh_token, verify_password
    security_imported = True
    print("Successfully imported 'security' functions in users/router.py.")
except ImportError as e:
    print(f"Critical Error during import of 'security' functions in users/router.py: {e}.")
    def create_access_token(data): return "fake_access_token"
    def create_refresh_token(data): return "fake_refresh_token"
    def verify_password(p1, p2): return False

# NEW: Attempt to import actual dependencies from core.dependencies
dependencies_imported_correctly = False
try:
    from backend.app.core.dependencies import get_db, get_current_user
    dependencies_imported_correctly = True
    print("Successfully imported 'get_db' and 'get_current_user' from core.dependencies in users/router.py.")
except ImportError as e:
    print(f"Critical Error importing dependencies from core.dependencies in users/router.py: {e}. Using local placeholders for get_db/get_current_user.")
    # Define local placeholders if import from core.dependencies fails
    def get_db(): # type: ignore
        print("Warning: users/router.py - Using local placeholder get_db due to import error from core.dependencies.")
        yield None
    async def get_current_user() -> Optional[models.User]: # type: ignore
        print("Warning: users/router.py - Using local placeholder get_current_user due to import error from core.dependencies.")
        return None
# END NEW

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserRead if schemas_imported else Any, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate if schemas_imported else Any, db: Session = Depends(get_db)): # MODIFIED Depends
    if not crud_imported or not schemas_imported: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server configuration error: User modules not loaded.")
    # MODIFIED DB Check logic
    if not db:
        if dependencies_imported_correctly:
            # This means the actual get_db from dependencies.py failed or returned None unexpectedly
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database service not available (actual dependency issue).")
        else:
            # This means we are using the local placeholder get_db defined in this file
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database service not available (local placeholder get_db in use).")
    
    db_user_by_username = crud.get_user_by_username(db, username=user.username) # type: ignore
    db_user_by_email = crud.get_user_by_email(db, email=user.email) # type: ignore
    
    if db_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    if db_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    created_user = crud.create_user(db=db, user=user) # type: ignore
    if not created_user: 
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create user (crud.create_user returned None).")
    return created_user


@router.post("/login", response_model=schemas.Token if schemas_imported else Any)
async def login_for_access_token(form_data: schemas.LoginCredentials if schemas_imported else Any, db: Session = Depends(get_db)): # MODIFIED Depends
    if not crud_imported or not security_imported or not schemas_imported:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server configuration error: Auth modules not loaded.")
    # MODIFIED DB Check logic
    if not db:
        if dependencies_imported_correctly:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database service not available (actual dependency issue).")
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database service not available (local placeholder get_db in use).")
            
    user_obj = crud.get_user_by_username(db, username=form_data.username) # type: ignore
    
    if not user_obj or not hasattr(user_obj, 'hashed_password') or not hasattr(user_obj, 'is_active') or not hasattr(user_obj, 'username'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password (user data missing or incomplete).",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user_obj.hashed_password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user_obj.is_active: # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    access_token = create_access_token(data={"sub": user_obj.username}) # type: ignore
    refresh_token = create_refresh_token(data={"sub": user_obj.username}) # type: ignore
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=Optional[schemas.UserRead] if schemas_imported else Any)
async def read_users_me(current_user: Optional[models.User] = Depends(get_current_user)): # MODIFIED Depends
    if not schemas_imported: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server configuration error: User schema not loaded.")

    if not current_user:
        if dependencies_imported_correctly:
             # This means actual get_current_user returned None (e.g. token invalid, user not found)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated or user not found.")
        else:
            # This means we are using the local placeholder get_current_user
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated (local placeholder get_current_user in use).")
    return current_user
