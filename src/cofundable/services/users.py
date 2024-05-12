"""Handle business logic related to Cofundable users."""

from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from cofundable.models.user import User
from cofundable.schemas.user import UserRequestSchema, UserUpdateSchema
from cofundable.services.accounts import (
    Account,
    AccountSchema,
    account_service,
)
from cofundable.services.base import CRUDBase


class UserCRUD(CRUDBase[User, UserRequestSchema, UserUpdateSchema]):
    """Manage CRUD operations for the User model."""

    def create(
        self,
        db: Session,
        *,
        data: UserRequestSchema,
        defer_commit: bool = False,  # optionally defer commit
    ) -> User:
        """Create a new user with an account balance of 0."""
        # create a new user and an associated account
        user = self.model(id=uuid4(), **jsonable_encoder(data))
        user.account = self._create_new_account(db, name=data.handle)
        # optionally commit before returning user
        if defer_commit:
            return user
        return self.commit_changes(db, user)

    def get_user_by_handle(self, db: Session, handle: str) -> User | None:
        """
        Find a user by their handle, if the handle exists in the system.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        handle: str
            The handle for the user to return

        Returns
        -------
        User | None
            Returns the matching user as an instance of the User model if found
            or returns None if no match is found

        """
        stmt = select(User).where(User.handle == handle)
        return db.execute(stmt).scalar()

    def _create_new_account(self, db: Session, *, name: str) -> Account:
        """Create an account for a new user with a balance of 0."""
        account_data = AccountSchema(name=name, balance=0)
        return account_service.create(db, data=account_data, defer_commit=True)


user_service = UserCRUD(model=User)
