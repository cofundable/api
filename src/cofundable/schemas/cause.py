"""
Declare the schema for a cause in Cofundable.

Causes represent organizations, initiatives, and projects that need funding
and resources.
"""

from pydantic import BaseModel, Field

from cofundable.schemas.base import UUIDAuditResponseBase


class CauseBase(BaseModel):
    """Base schema for a cause, with fields shared by POST, PUT, and GET."""

    name: str
    description: str
    handle: str
    tags: list[str] = Field(default=[])


class CauseRequestSchema(CauseBase):
    """Request schema for a cause that excludes read only fields."""


class CauseResponseSchema(CauseBase, UUIDAuditResponseBase):
    """Response schema for a cause that includes id, created_at, and updated_at."""
