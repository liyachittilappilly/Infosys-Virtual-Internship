from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────
#  REQUEST SCHEMAS (incoming data)
# ─────────────────────────────────────────────


class UserRegister(BaseModel):
    """Schema for user registration request."""

    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="SecurePass123")


class UserLogin(BaseModel):
    """Schema for user login (used internally; login endpoint uses OAuth2 form)."""

    username: str
    password: str


# ─────────────────────────────────────────────
#  RESPONSE SCHEMAS (outgoing data)
# ─────────────────────────────────────────────


class UserResponse(BaseModel):
    """Schema for returning user data (password excluded)."""

    id: int
    username: str
    email: str
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}  # Enables ORM mode (Pydantic v2)


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
