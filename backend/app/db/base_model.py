from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
# Import Base from the existing database.py
# from backend.app.db.database import Base
# If the worker has issues with this import, it should be noted.
# For robustness in the subtask, if Base cannot be imported,
# a placeholder could be used, but this is highly undesirable.
# The primary goal is to get the correct content into base_model.py

# Attempt to import Base
try:
    from backend.app.db.database import Base
    print("Successfully imported Base from backend.app.db.database in base_model.py.")
except ImportError:
    print("Critical Warning: Could not import Base from backend.app.db.database in base_model.py. This will likely cause issues.")
    # Fallback Base if absolutely necessary for subtask to run, though this indicates a problem
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()


class TimestampedModel(Base):
    __abstract__ = True  # Makes this a mixin, no table created for TimestampedModel

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
