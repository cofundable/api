"""
Declare the schema for a cause in Cofundable.

Causes represent organizations, initiatives, and projects that need funding
and resources.
"""

from pydantic import BaseModel, Field, computed_field

from cofundable.schemas.base import BASE_EXAMPLE, UUIDAuditResponseBase
from cofundable.schemas.tag import TagSchema

CAUSE_EXAMPLE: dict[str, str | list] = {
    "name": "Waverly Mutual Aid",
    "description": "A mutual aid group for the Waverly community in Baltimore",
    "handle": "waverly-mutual-aid",
    "tags": [
        "mutual-aid",
        "community-group",
    ],
}


class CauseBase(BaseModel):
    """Base schema for a cause, with fields shared by POST, PUT, and GET."""

    name: str
    handle: str
    description: str | None = None


class CauseRequestSchema(CauseBase):
    """Request schema for a cause that excludes read only fields."""

    tags: list[str] = Field(default=[])

    model_config = {"json_schema_extra": {"examples": [{**CAUSE_EXAMPLE}]}}


class CauseResponseSchema(CauseBase, UUIDAuditResponseBase):
    """Response schema for a cause that includes id, created_at, and updated_at."""

    tags: list[TagSchema] = Field(default=[])

    @computed_field
    def tag_names(self) -> list[str]:
        """Pluck the names of the tags associated with this cause."""
        if self.tags:
            return [tag.name for tag in self.tags]  # pylint: disable=E1133
        return []

    model_config = {
        "json_schema_extra": {"examples": [{**BASE_EXAMPLE, **CAUSE_EXAMPLE}]},
    }
