"""
Create the database models for the Cofundable API resources.

Note:
----
All of the models need to be imported here in order to be registered by Alembic,
so that the migration scripts are auto-generated correctly


"""

__all__ = ["UUIDAuditBase", "Cause", "Tag"]

from cofundable.models.base import UUIDAuditBase
from cofundable.models.cause import Cause
from cofundable.models.tag import Tag
