"""Create a CRUDBase class that other services can inherit from."""

from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from cofundable.models.base import UUIDAuditBase

ModelTypeT = TypeVar("ModelTypeT", bound=UUIDAuditBase)
CreateSchemaTypeT = TypeVar("CreateSchemaTypeT", bound=BaseModel)
UpdateSchemaTypeT = TypeVar("UpdateSchemaTypeT", bound=BaseModel)


class CRUDBase(Generic[ModelTypeT, CreateSchemaTypeT, UpdateSchemaTypeT]):
    """
    CRUD class with default methods to Create, Read, Update, Delete (CRUD).

    Parameters
    ----------
    model: Type[ModelTypeT]
        A SQLAlchemy model class for which CRUD operations will be supported
    schema: Type[BaseModel]
        A Pydantic model (schema) class to use to return the

    """

    def __init__(self, model: Type[ModelTypeT]) -> None:
        """Init the CRUD class with a given SQLAlchemy model."""
        self.model = model

    def get(self, db: Session, row_id: UUID) -> ModelTypeT | None:
        """
        Use the primary key to return a single record from the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        row_id: UUID
            The value of the primary key used to retrieve the record

        Returns
        -------
        Optional[ModelTypeT]
            Returns an instance of the SQLAlchemy model being queried if a row
            is found for the primary key value passed, or None otherwise

        """
        return db.get(self.model, row_id)

    def get_all(
        self,
        db: Session,
    ) -> Sequence[ModelTypeT]:
        """
        Return all of the entries from the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        skip: int, optional
            The number of rows to skip in the table before returning a row
        limit: int, optional
            The maximum number of rows to return in the query result

        Returns
        -------
        List[ModelTypeT]
            Returns a list of instances of the SQLAlchemy model being queried

        """
        stmt = sa.select(self.model)
        return db.execute(stmt).scalars().all()

    def create(
        self,
        db: Session,
        *,
        data: CreateSchemaTypeT,  # must be passed as keyword argument
    ) -> ModelTypeT:
        """
        Insert a new row into the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        data: CreateSchemaTypeT
            The instance of the Pydantic schema that contains the data used to
            insert a new row in the database

        """
        data = jsonable_encoder(data)  # makes data JSON-compatible
        record = self.model(id=uuid4(), **data.model_dump())
        return self.commit_changes(db, record)

    def update(
        self,
        db: Session,
        *,
        record: ModelTypeT,
        update_obj: UpdateSchemaTypeT,
    ) -> ModelTypeT:
        """
        Update a record in the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        record: ModelTypeT
            Instance of the SQLAlchemy model that represents the row in the
            corresponding database table that will be updated
        update_obj: Union[UpdateSchemaTypeT, Dict[str, Any]]
            Either an instance of a Pydantic schema or a dictionary of values
            used to update the row in the database

        """
        # convert record to dict so we can access its fields
        current_data = jsonable_encoder(record)

        # get the update data in dict format
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.model_dump(exclude_unset=True)

        # update the record with the update data
        for field in current_data:
            if field in update_data:
                setattr(record, field, update_data[field])

        return self.commit_changes(db, record)

    def delete(self, db: Session, *, row_id: UUID) -> None:
        """
        Delete a record from the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        row_id: UUID
            The primary key value of the row that will be deleted

        """
        record = db.get(self.model, row_id)
        db.delete(record)
        db.commit()

    def commit_changes(self, db: Session, record: ModelTypeT) -> ModelTypeT:
        """Add changes to a session, commits them, and refreshes the record."""
        db.add(record)
        db.commit()
        db.refresh(record)  # issues a SELECT stmt to refresh values of record
        return record
