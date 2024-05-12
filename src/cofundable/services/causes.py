"""Handle business logic related to Cofundable causes."""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from cofundable.models.cause import Cause
from cofundable.schemas.cause import CauseRequestSchema, CauseResponseSchema
from cofundable.services.accounts import (
    Account,
    AccountSchema,
    account_service,
)
from cofundable.services.base import CRUDBase
from cofundable.services.tags import Tag, tag_service


class CauseCRUD(CRUDBase[Cause, CauseRequestSchema, CauseResponseSchema]):
    """Manage CRUD operations for the Cause model."""

    def get_cause_by_handle(self, db: Session, handle: str) -> Cause | None:
        """Find a cause by its handle."""
        stmt = select(Cause).where(Cause.handle == handle)
        return db.execute(stmt).scalar()

    def create(
        self,
        db: Session,
        *,
        data: CauseRequestSchema,
        defer_commit: bool = False,  # optionally defer commit
    ) -> Cause:
        """Create a new cause."""
        # convert the cause data to a dict and remove tags to prevent an error
        cause_data = data.model_dump()
        cause_data.pop("tags")
        # create a new record in the cause table then assign the tags to it
        cause = self.model(id=uuid4(), **cause_data)
        cause.account = self._create_new_account(db, name=data.handle)
        cause.tags = self._get_tags(db, tags=data.tags)
        # optionally commit the new record before returning it
        if defer_commit:
            return cause
        return self.commit_changes(db, cause)

    def _get_tags(self, db: Session, tags: list[str]) -> set[Tag]:
        """Find or create the tags associated with a cause."""
        return tag_service.get_or_create_tags_by_name(
            db=db,
            tag_names=tags,
            defer_commit=True,
        )

    def _create_new_account(self, db: Session, name: str) -> Account:
        """Create a new account for this cause with a balance of 0."""
        account_data = AccountSchema(name=name, balance=0)
        return account_service.create(db, data=account_data, defer_commit=True)


cause_service = CauseCRUD(model=Cause)
