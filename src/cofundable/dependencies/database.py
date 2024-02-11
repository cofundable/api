# pylint: disable=invalid-name
"""Manage connection to the database using a SQLAlchemy session factory."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from cofundable import config
from cofundable.models.base import Base


def create_session_factory() -> sessionmaker:
    """Create a sessionmaker with database connection details."""
    engine = create_engine(config.settings.DATABASE_URL, pool_pre_ping=True)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Yield a connection to the database to manage transactions.

    Yields
    ------
    Session
        A SQLAlechemy session that manages a connection to the database

    """
    SessionFactory = create_session_factory()  # noqa: N806

    try:
        db = SessionFactory()
        yield db
    finally:
        db.close()


def init_test_db(db: Session, *, testing: bool = False) -> None:
    """
    Initialize the database for unit testing or for alembic migrations.

    Parameters
    ----------
    db: Session
        An instance of SessionLocal that creates the db engine and organizes
        calls to the database in a transaction
    testing: bool, optional
        Indicates whether to initialize the database in testing mode, which
        creates all of the tables from metadata instead of using Alembic.
        Default is to use Alembic migrations, see Notes below for details.

    Warning
    -------
    This function should only ever be called with testing=True during unit
    testing and the early stages of development. Doing so will create all of
    the tables from metadata. In all other cases (integration testing, QA
    testing, etc.) testing should remain False and tables should be created
    using Alembic migrations.

    """
    if testing:
        Base.metadata.drop_all(bind=db.get_bind())  # drop all existing tables
        Base.metadata.create_all(bind=db.get_bind())  # recreate all tables
