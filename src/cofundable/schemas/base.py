"""Create a base schema that other schemas can inherit from."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UUIDAuditResponseBase(BaseModel):
    """Base schema for response models that include a set of default fields."""

    id: UUID
    created_at: datetime
    updated_at: datetime
