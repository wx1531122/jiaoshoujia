from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from backend.app.db.database import Base

class TimestampedModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Optional: If you want to automatically generate table names
    # based on class names (e.g., UserProfile class -> user_profile table)
    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.lower() + "s" # Example: "users"
        # Or a more robust way to convert CamelCase to snake_case:
        # import re
        # return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower() + "s"
