"""Handle business logic related to Cofundable bookmarks."""

from uuid import UUID, uuid4

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from cofundable.errors import CauseHandleNotFoundError
from cofundable.models.bookmark import Bookmark
from cofundable.schemas.bookmark import (
    BookmarkCreateSchema,
    BookmarkUpdateSchema,
)
from cofundable.services.base import CRUDBase
from cofundable.services.causes import cause_service

BaseClasses = CRUDBase[
    Bookmark,
    BookmarkCreateSchema,
    BookmarkUpdateSchema,
]


class BookmarkCRUD(BaseClasses):
    """Manage CRUD operations for the Bookmark model."""

    def create(self, db: Session, *, data: BookmarkCreateSchema) -> Bookmark:
        """Create a new bookmark."""
        record = self.model(id=uuid4(), **data.model_dump())
        return self.commit_changes(db, record)

    def get_bookmarks_for_user(self, user_id: UUID) -> Select:
        """Query a user's bookmarks so that the results can be paginated."""
        return select(Bookmark).where(Bookmark.user_id == user_id)

    def get_bookmark_by_user_and_cause(
        self,
        db: Session,
        *,
        user_id: UUID,
        cause_id: UUID,
    ) -> Bookmark | None:
        """Find a bookmark by its user_id and cause_id."""
        stmt = select(self.model)
        stmt = stmt.where(self.model.cause_id == cause_id)
        stmt = stmt.where(self.model.user_id == user_id)
        return db.execute(stmt).scalar()

    def bookmark_cause_for_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        cause_handle: str,
    ) -> Bookmark:
        """Bookmark a cause for a user using the cause's handle."""
        cause = cause_service.get_cause_by_handle(db, cause_handle)
        if not cause:
            raise CauseHandleNotFoundError(handle=cause_handle)
        bookmark = self.get_bookmark_by_user_and_cause(
            db=db,
            user_id=user_id,
            cause_id=cause.id,
        )
        if bookmark:
            return bookmark
        return self.create(
            db=db,
            data=BookmarkCreateSchema(user_id=user_id, cause_id=cause.id),
        )


bookmark_service = BookmarkCRUD(model=Bookmark)
