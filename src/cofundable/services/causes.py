"""Handle business logic related to Cofundable causes."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from cofundable.models.cause import Cause
from cofundable.schemas.cause import CauseRequestSchema, CauseResponseSchema
from cofundable.services.base import CRUDBase
from cofundable.services.tags import tag_service


class CauseCRUD(CRUDBase[Cause, CauseRequestSchema, CauseResponseSchema]):
    """Manage CRUD operations for the Cause model."""

    def create(
        self,
        db: Session,
        *,
        data: CauseRequestSchema,
    ) -> Cause:
        """Create a new cause."""
        # get or create the tags that need to be assigned to the cause
        tag_names = data.tags
        tags = tag_service.get_or_create_tags_by_name(
            db=db,
            tag_names=tag_names,
        )
        # convert the cause data to a dict and remove tags to prevent an error
        cause_data = jsonable_encoder(data)
        cause_data.pop("tags")
        # create a new record in the cause table then assign the tags to it
        cause = self.model(id=uuid4(), **cause_data)
        cause.tags.update(tags)
        # commit the new record to the db and return it
        return self.commit_changes(db, cause)


def create_cause(data: CauseRequestSchema) -> CauseResponseSchema:
    """Create a new cause and return the resulting record."""
    now = datetime.now(timezone.utc)
    return CauseResponseSchema(
        **data.model_dump(),
        id=uuid4(),
        updated_at=now,
        created_at=now,
    )


def list_causes() -> list[CauseResponseSchema]:
    """Return a list of causes, optionally filtered by a set of fields."""
    now = datetime.now(timezone.utc)
    return [
        CauseResponseSchema(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            name="Acme",
            description="Test description",
            handle="acme",
        ),
    ]


cause_service = CauseCRUD(model=Cause)
