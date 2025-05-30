from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Attempt to import local modules. Critical for functionality.
# Fallbacks are for ensuring subtask can run if environment is broken.
users_router_imported = False # Initialize flags
db_utils_imported = False

# Import Starlette's HTTPException for broader handler registration
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import custom exceptions and their handlers
from app.core.exceptions import DetailedHTTPException
from app.core.error_handlers import (
    detailed_http_exception_handler,
    starlette_http_exception_handler
    # fastapi_http_exception_handler # Not including this one for now
    # generic_exception_handler 
)

try:
    from app.users import router as auth_router # Corrected import
    users_router_imported = True
    from app.db.database import create_db_and_tables # Corrected import
    db_utils_imported = True
    # Optional: from app.core.config import settings (if needed directly in main)
    print("Successfully imported auth_router and create_db_and_tables in main.py.")
except ImportError as e:
    print(f"Critical Error during import in main.py: {e}. API will be non-functional or limited.")
    # Define placeholders if absolutely necessary for the subtask to run
    from fastapi import APIRouter
    if not users_router_imported: # Check if this specific import failed
        auth_router = APIRouter() # Empty router
        print("Warning: Using placeholder auth_router in main.py.")
    if not db_utils_imported: # Check if this specific import failed
        def create_db_and_tables():
            print("Warning: Using placeholder create_db_and_tables in main.py. Database not initialized.")
    # Ensure flags reflect the actual success/failure of each import
    # (already handled by initializing to False and setting to True in try)


app = FastAPI(
    title="My Recovered FastAPI Application",
    version="0.1.1", # Slightly different version for recovery
    description="This is the recovered backend application."
)

# Register custom exception handlers
app.add_exception_handler(DetailedHTTPException, detailed_http_exception_handler)
# This will handle both FastAPI's HTTPException and Starlette's HTTPException
# as FastAPI.HTTPException inherits from StarletteHTTPException.
app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
# If you needed to handle FastAPI's HTTPException differently than Starlette's (rare),
# you would register it separately and potentially before StarletteHTTPException,
# or ensure your handler checks the exact type. For now, starlette_http_exception_handler
# will cover both, providing consistent formatting.
# app.add_exception_handler(FastAPIHTTPException, fastapi_http_exception_handler) 
# app.add_exception_handler(Exception, generic_exception_handler) # Generic fallback

# CORS Configuration
origins = [
    "http://localhost",         # Common local dev
    "http://localhost:3000",    # Common React dev port
    "http://localhost:5173",    # Common Vite dev port
    "http://127.0.0.1:5173",   # Another Vite dev host
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Can be ["*"] for permissive local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
if users_router_imported:
    app.include_router(auth_router, prefix="/api/v1") # Adding a common API prefix
else:
    print("Warning: Auth router not included in main.py due to import failure.")

# Startup Event for Database Initialization
@app.on_event("startup")
async def on_startup():
    if db_utils_imported:
        print("Application startup: Initializing database...")
        create_db_and_tables()
        print("Database tables created/verified.")
    else:
        print("Warning: Database initialization skipped in main.py due to import failure of create_db_and_tables.")

# Root Endpoint for Testing
@app.get("/")
async def root():
    return {"message": "Welcome to the Recovered API. Navigate to /docs for API documentation."}

# Optional: Add uvicorn run command example in comments for convenience
# if __name__ == "__main__":
#     import uvicorn
#     # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, app_dir="backend/app")
#     # Note: app_dir might be tricky depending on execution context.
#     # Usually run from the directory containing `backend` or from `backend/` itself.
#     uvicorn.run(app, host="0.0.0.0", port=8000)
