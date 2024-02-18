"""Create a base schema that other schemas can inherit from."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

BASE_EXAMPLE = {
    "id": "ad83342a-e81d-46d0-9009-36e89dc72d1c",
    "created_at": "2022-04-23T18:25:43.511Z",
    "updated_at": "2022-04-28T16:35:12.344Z",
}


class UUIDAuditResponseBase(BaseModel):
    """Base schema for response models that include a set of default fields."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
