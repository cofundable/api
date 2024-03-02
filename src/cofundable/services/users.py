"""Handle business logic related to Cofundable users."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from cofundable.models.user import User
from cofundable.schemas.user import UserRequestSchema, UserResponseSchema
from cofundable.services.base import CRUDBase


class UserCRUD(CRUDBase[User, UserRequestSchema, UserResponseSchema]):
    """Manage CRUD operations for the Cause model."""

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


user_service = UserCRUD(model=User)
