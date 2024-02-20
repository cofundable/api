"""
Declare the schemas for a user's bookmarks in Cofundable.

Bookmarks are causes that a user has saved so they can revisit them later.
Users who have bookmarked a cause appear in that cause's list of followers.
"""

from uuid import UUID

from pydantic import BaseModel

from cofundable.schemas.base import BASE_EXAMPLE, UUIDAuditResponseBase
from cofundable.schemas.cause import CAUSE_EXAMPLE, CauseResponseSchema

BOOKMARK_EXAMPLE: dict[str, str | list | dict] = {
    **BASE_EXAMPLE,
    "cause": CAUSE_EXAMPLE,
}


class BookmarkCreateSchema(BaseModel):
    """Schema that is used by the BookmarkCRUD class to create a Bookmark."""

    cause_id: UUID
    user_id: UUID


class BookmarkUpdateSchema(BaseModel):
    """Schema that is used by the BookmarkCRUD class to update a Bookmark."""


class BookmarkResponseSchema(UUIDAuditResponseBase, BaseModel):
    """Base schema for a cause, with fields shared by POST, PUT, and GET."""

    cause: CauseResponseSchema

    model_config = {"json_schema_extra": {"examples": [{**BOOKMARK_EXAMPLE}]}}
