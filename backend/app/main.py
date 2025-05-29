from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.users import router as auth_router
from backend.app.db.database import create_db_and_tables
# Optional: from backend.app.core.config import settings # For testing settings loading

# Create FastAPI App Instance
app = FastAPI(title="My FastAPI Application", version="0.1.0")

# Configure CORS
# Adjust origins as needed for your frontend application
origins = [
    "http://localhost",         # Common for local development
    "http://localhost:3000",    # Common for React frontend
    "http://localhost:5173",    # Common for Vite/Vue frontend
    "http://localhost:8000",    # If uvicorn runs on default 8000
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for allowing all origins during development
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods
    allow_headers=["*"],    # Allows all headers
)

# Include Routers
app.include_router(auth_router, prefix="/api/v1") # Added a common prefix for API versioning

# Add Startup Event for Database Initialization
@app.on_event("startup")
async def on_startup():
    print("Application startup: Initializing database...")
    create_db_and_tables()
    print("Database tables created/verified.")
    # Optional: Test settings loading
    # print(f"Settings loaded: DB URL starts with {settings.DATABASE_URL[:20]}...")


# Optional: Add a Root Endpoint for Testing
@app.get("/")
async def root():
    return {"message": "Welcome to the API. Navigate to /docs for API documentation."}

# Example of how to run this app (for development):
# uvicorn backend.app.main:app --reload
# Ensure your PYTHONPATH is set correctly if running from outside the backend/app directory,
# or run from the directory containing `backend` like:
# python -m uvicorn backend.app.main:app --reload --app-dir .
# or if inside `backend` directory:
# python -m uvicorn app.main:app --reload --app-dir .
# If using an IDE, configure it to run uvicorn with the correct module path.
