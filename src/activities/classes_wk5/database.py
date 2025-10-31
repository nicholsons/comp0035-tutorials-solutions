""" Creates the database file with tables

Note:
    The models import is required for the create_all to create the tables.

    from activities.classes_wk5 import models

    `# noqa: F401` suppresses the linter warning of an unused import

    """
from importlib import resources

from sqlmodel import SQLModel, create_engine

from activities import classes_wk5
from activities.classes_wk5 import models  # noqa: F401

para_sqlmodel_db = resources.files(classes_wk5).joinpath("para_sqlmodel.sqlite")
sqlite_url = f"sqlite:///{str(para_sqlmodel_db)}"
engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
