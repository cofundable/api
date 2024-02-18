"""Handle business logic related to tags."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from cofundable.models.tag import Tag
from cofundable.schemas.tag import TagSchema
from cofundable.services.base import CRUDBase


class TagsCRUD(CRUDBase[Tag, TagSchema, TagSchema]):
    """Manage CRUD operations for tags."""

    def get_or_create_tags_by_name(
        self,
        db: Session,
        *,
        tag_names: list[str],
    ) -> set[Tag]:
        """Find a list of tag entries by name, or create them if they don't exist."""
        # find existing tags records by name
        tags = self.get_tags_by_name(db, tag_names=tag_names)
        existing_tags = {tag.name for tag in tags}
        # create new tag records if they don't exist
        for tag_name in tag_names:
            if tag_name not in existing_tags:
                tag_data = TagSchema(name=tag_name)
                tags.add(self.create(db=db, data=tag_data))
        # return existing and newly created tags
        return tags

    def get_tags_by_name(
        self,
        db: Session,
        *,
        tag_names: list[str],
    ) -> set[Tag]:
        """Find a list of tag entries by name."""
        stmt = select(Tag).where(Tag.name.in_(tag_names))
        return set(db.execute(stmt).scalars().all())


tag_service = TagsCRUD(model=Tag)
