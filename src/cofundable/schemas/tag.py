"""Declare the schemas for tags in Cofundable."""

from pydantic import BaseModel


class TagSchema(BaseModel):
    """Base schema for a tag, with common fields."""

    name: str
    description: str | None = None
