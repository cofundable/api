"""Handle business logic for accounts that store share balances in Cofundable."""

from cofundable.models.account import Account
from cofundable.schemas.account import AccountSchema
from cofundable.services.base import CRUDBase


class AccountCRUD(CRUDBase[Account, AccountSchema, AccountSchema]):
    """Manage CRUD operations for the Cause model."""


account_service = AccountCRUD(model=Account)
