from sqlalchemy.orm import Session
from app import models
from app.auth import hash_password
from app.schemas import UserRegister


def get_user_by_username(db: Session, username: str):
    """Fetch a user by their username."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Fetch a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """Fetch a user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user_data: UserRegister) -> models.User:
    """
    Create a new user:
    - Hash the password before storing
    - Commit to DB and refresh the instance
    """
    hashed = hash_password(user_data.password)
    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user: models.User) -> models.User:
    """Set a user's is_active flag to False."""
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user
