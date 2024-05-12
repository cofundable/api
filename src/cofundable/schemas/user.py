"""Declare the schemas for users in Cofundable's API."""

from pydantic import BaseModel

from cofundable.schemas.base import BASE_EXAMPLE, UUIDAuditResponseBase

USER_EXAMPLE: dict[str, str | list] = {
    "name": "Alice Williams",
    "handle": "alicewilliams",
    "bio": "I'm passionate about grassroots organizing for climate justice.",
}


class UserBase(BaseModel):
    """Base schema for a user, with fields shared by POST, PUT, and GET."""

    name: str
    handle: str
    bio: str | None = None


class UserUpdateSchema(BaseModel):
    """Schema used to update the User model."""

    name: str | None = None
    handle: str | None = None
    bio: str | None = None


class UserRequestSchema(UserBase):
    """Request schema for a cause that excludes read-only fields."""

    model_config = {"json_schema_extra": {"examples": [{**USER_EXAMPLE}]}}


class UserResponseSchema(UUIDAuditResponseBase, UserBase):
    """Response schema for a cause that includes id, created_at, and updated_at."""

    model_config = {
        "json_schema_extra": {"examples": [{**BASE_EXAMPLE, **USER_EXAMPLE}]},
    }
