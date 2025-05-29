from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings

# SQLAlchemy Engine
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for ORM models
Base = declarative_base()

# Function to create database tables
def create_db_and_tables():
    """
    Creates all database tables defined by Base metadata.
    This function should be called once at application startup
    if the tables do not already exist.
    """
    Base.metadata.create_all(bind=engine)
