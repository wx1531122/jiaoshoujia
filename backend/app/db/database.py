from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Attempt to import actual settings, fallback to placeholder
actual_settings_imported = False
try:
    from app.core.config import settings # Assuming 'app' is a package
    actual_settings_imported = True
    print("Successfully imported actual settings in database.py.")
except ImportError as e:
    print(f"Warning: Could not import actual settings in database.py ({e}). Using placeholders.")
    class SettingsPlaceholder:
        DATABASE_URL: str = "postgresql://user:password@host:port/database_fallback"
    settings = SettingsPlaceholder() # Use placeholder if import fails

# If actual settings were not imported, the placeholder 'settings' is already defined.
# If they were, 'settings' from config is in scope.

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Conditional connect_args for SQLite
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to create database tables
def create_db_and_tables():
    """
    Creates all database tables defined by Base metadata.
    This function should be called once at application startup
    if the tables do not already exist.
    """
    Base.metadata.create_all(bind=engine)

# Optional: A dependency to get DB session (can also be in dependencies.py)
# def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
