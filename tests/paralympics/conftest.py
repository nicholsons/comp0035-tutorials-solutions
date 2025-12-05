"""
The SQLModel documentation for testing focuses on FastAPI apps which you don't have.
The session fixture however can be used:
https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#boilerplate-code

The following tutorial covers testing using only SQLModel:
 https://pytest-with-eric.com/database-testing/pytest-sql-database-testing/
"""

from pathlib import Path

import pytest
from sqlalchemy import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from para_app.database import add_data, drop_data
from para_app.models import *


# Adapted from https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#boilerplate-code
# The @pytest.fixture() decorator on top of the function tells pytest this is a fixture function
@pytest.fixture(scope="function")
def engine_fixture():
    """ Engine fixture for testing the database

     This fixture creates:
     - the custom engine
     - the tables

     Then yields the engine object. The thing is 'yielded is what will be available to the test
     functions, i.e. the engine in this case.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    SQLModel.metadata.create_all(engine)
    yield engine


@pytest.fixture(scope="function")
def session_fixture(engine_fixture):
    """ Session fixture for testing the database

     This fixture takes the engine and then creates and yields the session object.

     The thing is 'yield'ed is what will be available to the test function, i.e. the session object.

    Use yield so that pytest comes back to execute "the rest of the code" in this function once the
    testing function is done.

    There is no further "rest of the code" after the yield, but the end of the 'with' block will
    close the session.

    By using yield, pytest will:

        - run the first part
        - create the session object
        - give it to the test function
        - run the test function
        - once the test function is done, it will continue right after the yield, and will
        close the session object at the end of the 'with' block.
    """
    with Session(engine_fixture) as session:
        yield session


@pytest.fixture(scope="function")
def db_with_data(engine_fixture):
    """ Re-creates the data in the database for each test function

    The data volume is quite small for this database, so all data is being added each time.
    For a larger database load sample data for testing.

    This fixture has code after the yield which runs at the end of each test as the scope of the
    fixture is set to 'function'.

    """
    add_data(engine_fixture)
    yield
    drop_data(engine_fixture)
