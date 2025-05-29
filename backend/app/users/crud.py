from sqlalchemy.orm import Session
from backend.app.users.models import User
from backend.app.users.schemas import UserCreate
from backend.app.core.security import get_password_hash

# Get user by ID
def get_user(db: Session, user_id: int) -> User | None:
    """
    Queries the database for a user by their ID.
    """
    return db.query(User).filter(User.id == user_id).first()

# Get user by username
def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Queries the database for a user by their username.
    """
    return db.query(User).filter(User.username == username).first()

# Get user by email
def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Queries the database for a user by their email address.
    """
    return db.query(User).filter(User.email == email).first()

# Create a new user
def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    - Hashes the user's plain password.
    - Adds the new user to the session, commits, and refreshes.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
