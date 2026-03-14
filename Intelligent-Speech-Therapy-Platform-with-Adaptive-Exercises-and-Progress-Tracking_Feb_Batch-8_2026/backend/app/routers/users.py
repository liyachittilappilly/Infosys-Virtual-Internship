from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.schemas import UserResponse
from app import models

router = APIRouter(prefix="/users", tags=["Users"])


# ─────────────────────────────────────────────
#  GET /users/me
# ─────────────────────────────────────────────


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user details",
)
def get_me(current_user: models.User = Depends(get_current_user)):
    """
    Returns the profile of the currently authenticated user.

    Requires a valid **Bearer JWT token** in the Authorization header.
    """
    return current_user
