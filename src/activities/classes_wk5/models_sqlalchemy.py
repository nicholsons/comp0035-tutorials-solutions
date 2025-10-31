# This example has all the code in a single file.
# In an app the models classes would likely be defined in a modules named 'modles.py'
# and the code to create the database elsewhere.
from __future__ import annotations

from datetime import date
from typing import List

from sqlalchemy import Date, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


# Declarative base class
class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "person"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    dob: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Relationship
    pets: Mapped[List["Pet"]] = relationship(back_populates="owner")


class Pet(Base):
    __tablename__ = "pet"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("person.id"))
    # Relationship
    owner: Mapped["Person"] = relationship(back_populates="pets")


if __name__ == '__main__':
    # Create the engine
    # Creates the database file if it does not already exist
    db_url = f"sqlite:///pets.sqlite"
    engine = create_engine(db_url)

    # Create the tables defined in the code above
    Base.metadata.create_all(engine)

    # Create and add data
    # Create the owner
    owner = Person(first_name="Some", last_name="Person")
    # Create the pet
    pet = Pet(name="Fido")
    # Append the pet to the list of pets for this person (owner)
    owner.pets.append(pet)
    # Owner with DOB so you can see that SQLAlchemy can add a date to a SQLite database
    date_birth = date(2010, 1, 1)
    owner_two = Person(first_name="AN", last_name="Other", dob=date_birth)

    with Session(engine) as session:
        # Since the pet is already appended to the owner, you only need to add the owner to commit both owner and pet
        session.add_all([owner, owner_two])
        session.commit()
