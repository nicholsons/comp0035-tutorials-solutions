from datetime import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel, Session, create_engine, text, select


class Error(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    error_code: str = Field(unique=True)
    error_description: str

    occurrences: List['Occurrence'] = Relationship(back_populates="error")


class Occurrence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str
    software_used: str
    error_id: int | None = Field(default=None, foreign_key="error.id")
    error: Error | None = Relationship(back_populates="occurrences")


def create_db(engine):
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    add_sample_data(engine)


def add_sample_data(engine):
    with Session(engine) as session:
        errors = [
            Error(error_code="E001", error_description="Null pointer exception"),
            Error(error_code="E002", error_description="Database connection failed"),
            Error(error_code="E003", error_description="File not found"),
        ]
        session.add_all(errors)
        session.commit()
        occurrences = [
            Occurrence(date=datetime.now().strftime("%Y-%m-%d"), software_used="AppX", error_id=1),
            Occurrence(date=datetime.now().strftime("%Y-%m-%d"), software_used="AppY", error_id=2),
            Occurrence(date=datetime.now().strftime("%Y-%m-%d"), software_used="AppZ", error_id=3),
            Occurrence(date=datetime.now().strftime("%Y-%m-%d"), software_used="AppX", error_id=2),
        ]
        session.add_all(occurrences)
        session.commit()


def database_location_incorrect():
    engine = create_engine("sqlite:///data/errordbsqlite", echo=True)
    create_db(engine)


def duplicate_value(engine):
    with Session(engine) as session:
        e = Error(error_code="E001", error_description="Null pointer exception")
        session.add(e)
        session.commit()


def invalid_column_name(engine):
    with Session(engine) as session:
        e = Error(error_codes="E001", error_description="Null pointer exception")
        session.add(e)
        session.commit()


def no_records_found(engine):
    with Session(engine) as session:
        statement = select(Error).where(Error.error_code == "E999")
        result = session.exec(statement)
        print(result.first())



if __name__ == '__main__':
    # Uncomment and run each of these in turn to see the exceptions; then add try/except to the functions

    # Creates an in-memory database, ie not on file
    engine = create_engine("sqlite:///:memory:", echo=True)
    create_db(engine)

    # database_location_incorrect()

    # duplicate_value(engine)

    # invalid_column_name(engine)

    # no_records_found(engine)
