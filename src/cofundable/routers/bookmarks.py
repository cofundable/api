"""Route API requests related to bookmarking causes."""

from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links import Page
from sqlalchemy.orm import Session

from cofundable.dependencies.auth import get_current_user
from cofundable.dependencies.database import get_db
from cofundable.models import Bookmark, User
from cofundable.schemas.bookmark import BookmarkResponseSchema
from cofundable.services.bookmarks import bookmark_service

bookmark_router = APIRouter(
    tags=["bookmarks"],
    responses={404: {"description": "Not found"}},
)


@bookmark_router.get(
    "/user/bookmarks/",
    summary="List current user's bookmarks",
    response_model=Page[BookmarkResponseSchema],
)
def list_bookmarks_for_current_user(
    db: Annotated[Session, Depends(get_db)],
    curr_user: Annotated[User, Depends(get_current_user)],
) -> Sequence[Bookmark]:
    """Fetch a paginated list of bookmarks for the currently authenticated user."""
    query = bookmark_service.get_bookmarks_for_user(curr_user.id)
    return paginate(conn=db, query=query)


@bookmark_router.put(
    "/user/bookmarks/{cause}",
    summary="Bookmark a cause for the current user",
    response_model=BookmarkResponseSchema,
    status_code=status.HTTP_200_OK,
)
def bookmark_cause_for_current_user(
    db: Annotated[Session, Depends(get_db)],
    curr_user: Annotated[User, Depends(get_current_user)],
    cause: str,
) -> Bookmark:
    """Add a cause to the currently authenticated user's list of bookmarks."""
    return bookmark_service.bookmark_cause_for_user(
        db,
        user_id=curr_user.id,
        cause_handle=cause,
    )
