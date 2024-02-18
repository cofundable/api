"""Handle business logic related to Cofundable causes."""

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


cause_service = CauseCRUD(model=Cause)
