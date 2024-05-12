"""Manage AuthN/AuthZ dependencies for Cofundable API."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from cofundable.dependencies.database import get_db
from cofundable.services.users import User, user_service


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Get the currently authenticated user and their scopes."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = db.execute(user_service.query_all()).scalar()
    if not user:
        raise credentials_exception
    return user
