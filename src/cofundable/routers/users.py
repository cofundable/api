"""Route API requests related to users."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from cofundable.dependencies.auth import get_current_user
from cofundable.dependencies.database import get_db
from cofundable.models import User
from cofundable.schemas.user import UserRequestSchema, UserResponseSchema
from cofundable.services.users import user_service

user_router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@user_router.get(
    "/user/",
    summary="Get the currently authenticated user",
    response_model=UserResponseSchema,
)
def get_current_logged_in_user(
    curr_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Fetch the details about the user who is currently logged in."""
    return curr_user


@user_router.post(
    "/users/",
    summary="Create a new user",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    db: Annotated[Session, Depends(get_db)],
    payload: UserRequestSchema,
) -> User:
    """Create a new user."""
    return user_service.create(db, data=payload)
