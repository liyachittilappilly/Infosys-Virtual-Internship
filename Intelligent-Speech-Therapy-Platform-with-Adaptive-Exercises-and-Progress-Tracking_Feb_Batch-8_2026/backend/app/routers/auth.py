from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.auth import (
    verify_password,
    create_access_token,
    get_current_user,
    blacklist_token,
    oauth2_scheme,
)
from app.database import get_db
from app.schemas import UserRegister, UserResponse, TokenResponse, MessageResponse
from app import models

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ─────────────────────────────────────────────
#  POST /auth/register
# ─────────────────────────────────────────────


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user account.

    - **username**: Unique username (3–50 chars)
    - **email**: Valid email address
    - **password**: Minimum 6 characters (stored as bcrypt hash)
    """
    # Check if username already exists
    if crud.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered. Please choose a different one.",
        )

    # Check if email already exists
    if crud.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email.",
        )

    new_user = crud.create_user(db, user_data)
    return new_user


# ─────────────────────────────────────────────
#  POST /auth/login
# ─────────────────────────────────────────────


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and receive a JWT access token",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login with **username** and **password** (form data).

    Returns a **Bearer JWT token** to use in protected endpoints.
    """
    # Look up user
    user = crud.get_user_by_username(db, form_data.username)

    # Validate credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please contact support.",
        )

    # Create token
    access_token = create_access_token(data={"sub": user.username})

    return TokenResponse(access_token=access_token, token_type="bearer")


# ─────────────────────────────────────────────
#  POST /auth/logout
# ─────────────────────────────────────────────


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout and invalidate the current JWT token",
)
def logout(
    token: str = Depends(oauth2_scheme),
    current_user: models.User = Depends(get_current_user),
):
    """
    Logout the currently authenticated user.

    Adds the current JWT token to a **blacklist** so it can no longer be used,
    even if it hasn't expired yet.
    """
    blacklist_token(token)
    return MessageResponse(
        message=f"User '{current_user.username}' successfully logged out."
    )
