""" Model classes for the paralympics database

Follows on from week 8 activity with validators and methods added to Games

"""
from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlmodel import CheckConstraint, Field, Relationship, SQLModel


class GamesHost(SQLModel, table=True):
    __tablename__ = "games_host"
    id: Optional[int] = Field(default=None, primary_key=True)
    games_id: int = Field(default=None, foreign_key="games.id")
    host_id: int = Field(default=None, foreign_key="host.id")


class GamesDisability(SQLModel, table=True):
    __tablename__ = "games_disability"
    id: Optional[int] = Field(default=None, primary_key=True)
    games_id: int = Field(default=None, foreign_key="games.id")
    disability_id: int = Field(default=None, foreign_key="disability.id")


class GamesTeam(SQLModel, table=True):
    __tablename__ = "games_team"
    id: Optional[int] = Field(default=None, primary_key=True)
    games_id: int = Field(default=None, foreign_key="games.id")
    team_id: str = Field(default=None, foreign_key="team.code")


class Games(SQLModel, table=True):
    __tablename__ = "games"
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str
    year: int
    start_date: Optional[str]
    end_date: Optional[str]
    countries: Optional[int]
    events: Optional[int]
    sports: Optional[int]
    participants_m: Optional[int]
    participants_f: Optional[int]
    participants: Optional[int]
    highlights: Optional[str]
    url: Optional[str]

    hosts: list["Host"] = Relationship(back_populates="games", link_model=GamesHost)
    disabilities: list["Disability"] = Relationship(back_populates="games", link_model=GamesDisability)
    teams: list["Team"] = Relationship(back_populates="games", link_model=GamesTeam)

    __table_args__ = (
        CheckConstraint("event_type IN ('winter', 'summer')"),
        CheckConstraint("year BETWEEN 1960 AND 9999")
    )

    # Validators more typically on the Pydantic schema
    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        allowed = ["winter", "summer"]
        value = value.lower()
        if value not in allowed:
            raise ValueError(f"{value} is not in {allowed}")
        return value

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        value = int(value)
        if value < 1960 or value > 9999:
            raise ValueError(f"{value} must be between 1960 and 9999")
        return value

    def calculate_duration(self) -> Optional[int]:
        """ Calculate the duration of the Paralympics

        Parses string start_date and end_date as dates and then calculates the difference in days.

        Returns:
            int: Duration in days

        Raises:
            ValueError: If the start date is greater than the end date
            ValueError: If the start date or the end date are None
            ValueError: end date is before the start date
        """

        if not self.start_date or not self.end_date:
            raise ValueError("Both start_date and end_date must be set to calculate duration.")

        try:
            start = datetime.strptime(self.start_date, "%d-%m-%Y").date()
            end = datetime.strptime(self.end_date, "%d-%m-%Y").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        if end < start:
            raise ValueError("end_date cannot be earlier than start_date.")

        return (end - start).days

    def calculate_fm_ratio(self) -> float:
        """ Calculates the ratio of female:male participants

        Pydantic and SQLAlchemy should validate that the values are integers

        Returns:
            ratio (float): ratio of female to male participants

        Raises:
            ValueError: If either participants_ or participants_f is None, 0 or negative
        """
        if self.participants_m is None or self.participants_f is None:
            raise ValueError("participants_m and participants_f must be set to calculate ratio.")
        m = self.participants_m
        f = self.participants_f
        if m == 0 or f == 0:
            raise ValueError("participants_m and participants_f must be non-zero.")
        if m < 0 or f < 0:
            raise ValueError("participants_m and participants_f must be non-negative.")
        return float(f) / float(m)


class Team(SQLModel, table=True):
    __tablename__ = "team"
    code: str = Field(primary_key=True)  # Not set by the database
    name: str
    region: Optional[str]
    member_type: str
    notes: Optional[str]
    country_id: Optional[str] = Field(default=None, foreign_key="country.id")

    games: list["Games"] = Relationship(back_populates="teams", link_model=GamesTeam)

    __table_args__ = (
        CheckConstraint("member_type IN ('country', 'team', 'dissolved', 'construct')"),
        CheckConstraint("region IN ('Asia', 'Europe', 'Africa', 'America', 'Oceania')")
    )

    @field_validator("member_type", mode="after")
    @classmethod
    def validate_member_type(cls, value: str) -> str:
        allowed = ["country", "team", "dissolved", "construct"]
        if value not in allowed:
            raise ValueError(f"{value} is not in {allowed}")
        return value

    @field_validator("region", mode="after")
    @classmethod
    def validate_region(cls, value: Optional[str]) -> Optional[str]:
        allowed = ["Asia", "Europe", "Africa", "America", "Oceania"]
        if value is not None and value not in allowed:
            raise ValueError(f"{value} is not in {allowed}")
        return value

    def __repr__(self) -> str:
        field_values = ", ".join(f"{name}={getattr(self, name)!r}" for name in self.model_fields.keys())
        return f"{self.__class__.__name__}({field_values})"

    def __str__(self) -> str:
        return f"{self.code} {self.name} is in {self.region} and is a {self.member_type}."


class Disability(SQLModel, table=True):
    __tablename__ = "disability"
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str

    games: list["Games"] = Relationship(back_populates="disabilities", link_model=GamesDisability)


class Host(SQLModel, table=True):
    __tablename__ = "host"
    id: Optional[int] = Field(default=None, primary_key=True)
    place_name: str = Field(unique=True)
    country_id: Optional[int] = Field(default=None, foreign_key="country.id")

    games: list["Games"] = Relationship(back_populates="hosts", link_model=GamesHost)


class Country(SQLModel, table=True):
    __tablename__ = "country"
    id: Optional[int] = Field(default=None, primary_key=True)
    country_name: str
