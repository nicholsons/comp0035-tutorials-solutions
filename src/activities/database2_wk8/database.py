""" Creates the database file with tables

Note:
    The models import is required for the create_all to create the tables.

    from activities.database2_wk8 import models

    """
from importlib import resources

from sqlmodel import SQLModel, create_engine, text

from activities import data, database2_wk8
from activities.database2_wk8 import models

student_db = resources.files(database2_wk8).joinpath("students.sqlite")
sqlite_url = f"sqlite:///{str(student_db)}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    """Creates all tables in the database.

        Enables foreign key support for SQLite.
    """
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))  # for SQLite foreign key support


def drop_db_and_tables():
    """ Drops all tables in the database."""
    SQLModel.metadata.drop_all(engine)
