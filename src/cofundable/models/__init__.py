"""
Create the database models for the Cofundable API resources.

Note:
----
All of the models need to be imported here in order to be registered by Alembic,
so that the migration scripts are auto-generated correctly


"""

__all__ = [
    "UUIDAuditBase",
    "Account",
    "Bookmark",
    "Cause",
    "Tag",
    "EntryType",
    "Transaction",
    "User",
]

from cofundable.models.account import Account
from cofundable.models.base import UUIDAuditBase
from cofundable.models.bookmark import Bookmark
from cofundable.models.cause import Cause
from cofundable.models.tag import Tag
from cofundable.models.transaction import EntryType, Transaction
from cofundable.models.user import User
