""" Example queries

Python classes are typically used when you need to encapsulate data and related functions.

So why not add the CRUD methods to the model classes?

You can do that. One reason you might not is the design principle, separation of concerns. Separation of concerns
helps to avoid large, bloated classes that can be harder to maintain, harder to re-use and harder to test.

You might decide to keep the models representing the data structure separate from the business logic handling services
such as validation and queries.

Developers using frameworks such as FastAPI often use an architecture that separates the app into layers:

- Models: to represent the data
- Schemas: using Pydantic for validation
- Services: for the business logic
- Routers (controllers): API end-points

This activity is only using SQLModel, though you can use Pydantic schemas in coursework 2 if you wish.
Do not use FastAPI for this coursework please, that is in COMP0034.
"""
from typing import Sequence

from sqlmodel import Session, func, select

from para_app.models import Country, Disability, Games, GamesHost, Host, Team


class QueryService:
    """ Class with database queries

        Use to demonstrate example queries in the tutorial.

        DEMO of all basic CRUD:
            Read all hosts
            Create a new host city
            Read the new host
            Update the host city name
            Delete the new host city

        Write queries for:
            DEMO: 1. List all Paralympics (games) with their year and type. Order by year.
            DEMO: 2. List all winter Paralympics (games) with host name(s) and year.
            3. Find all disabilities recorded in the database.
            4. Get all Paralympics (Games) that took place after the year 2000. Order by year.
            5. Find all teams from a specific region (e.g. Oceania). Order by team name.
            6. List all hosts located in a specific country (e.g., 'Italy') and the year they held the Paralympics.
            7. Show all Paralympics (games) along with their host city and host country.
            8. List all disabilities associated with each Paralympics (games).
            9. Find all teams that participated in a year and event_type (e.g., winter 2016).
            10. Find all the Paralympics that have competitors who are 'Amputees'
            11. **Update** the disability description 'Les Autres' to 'Other'
    """

    def __init__(self, eng):
        self.engine = eng

    def read_hosts(self) -> Sequence[Host]:
        with Session(self.engine) as session:
            statement = select(Host).order_by(Host.place_name)
            hosts = session.exec(statement).all()
            return hosts

    def create_host(self, place_name: str, country_name: str) -> Host:
        """
        Host has id, place_name and country_id
        Country has id, country_name
        UK is listed as 'Great Britain' in the country table
        """
        with Session(self.engine) as session:
            # Find the country_id
            statement = select(Country.id).where(Country.country_name == country_name)
            country_id = session.exec(statement).first()
            new_host = Host(place_name=place_name, country_id=country_id)
            session.add(new_host)
            session.commit()
            session.refresh(new_host)
            return new_host

    def read_host(self, host_id: int) -> Host:
        with Session(self.engine) as session:
            statement = select(Host).where(Host.id == host_id)
            host = session.exec(statement).first()
            # Alternatives:
            # host = session.exec(statement).one()  # .one() throws error if more than 1 result
            # host = session.get(Host, host_id)  # Shortcut for getting a row by its id
            return host

    def update_host(self, updated_host: Host) -> Host:
        with Session(self.engine) as session:
            session.add(updated_host)
            session.commit()
            session.refresh(updated_host)
            return updated_host

    def delete_host(self, host_id: int) -> None:
        """ Find the host that matches the host_id, then delete it """
        with Session(self.engine) as session:
            host = session.exec(select(Host).where(Host.id == host_id)).first()
            session.delete(host)
            session.commit()

    def query_games_year_type(self) -> Sequence:
        # 1. List all Paralympics (games) with their year and type. Order by year.
        statement = (
            select(Games.year, Games.event_type)
            .order_by(Games.year)
        )
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_games_type_with_host(self, event_type: str) -> Sequence:
        """ 2. List all winter Paralympics (games) with the host city name and year.
            SQL equivalent:
                SELECT host.place_name, games.year
                FROM games
                JOIN games_host AS games_host_1 ON games.id = games_host_1.games_id
                JOIN host ON host.id = games_host_1.host_id
                WHERE games.event_type = ?
                ORDER BY games.year
        """
        statement = (
            select(Host.place_name, Games.year)
            .join(Host, Games.hosts)  # using Games.hosts relationship
            .where(Games.event_type == event_type)
            .order_by(Games.year)
        )
        alternative_join_statement = (
            select(Host.place_name, Games.year)
            .join(GamesHost, Games.id == GamesHost.games_id)  # using `JOIN ... ON ...`
            .join(Host, Host.id == GamesHost.host_id)
            .where(Games.event_type == event_type)
            .order_by(Games.year)
        )
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_disabilities(self) -> Sequence:
        # 3. Find all disabilities recorded in the database.
        statement = select(Disability)
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_games_after_year(self, year: int) -> Sequence:
        # 4. Get all Paralympics (Games) that took place after the year 2000.
        statement = select(Games).where(Games.year > 2000).order_by(Games.year)
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_region_teams(self, region: str) -> Sequence:
        # 5. Find all teams from a specific region (e.g. Oceania).
        statement = select(Team).where(Team.region == region)
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_host_country(self, country: str) -> Sequence:
        # 6. List all hosts located in a specific country (e.g., 'Italy') and the year they held the Paralympics.
        statement = (
            select(Host.place_name, Games.year)
            .join(Games, Host.games)
            .join(Country, Host.country_id == Country.id)
            .where(Country.country_name == country)
        )
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_games_host_country(self) -> Sequence:
        # 7. Show all Paralympics (games) along with their host city and host country.
        statement = (
            select(Games.year, Games.event_type, Host.place_name, Country.country_name)
            .join(Host, Games.hosts)
            .join(Country, Host.country_id == Country.id)
        )
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_disabilities_by_games(self) -> Sequence:
        # 8. List all disabilities associated with each Paralympics (games).
        statement = (
            select(
                Games.year,
                Games.event_type,
                func.group_concat(Disability.description, ', ').label("disabilities")
            )
            .join(Disability, Games.disabilities)
            .group_by(Games.year, Games.event_type)
        )
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_teams_year(self, year: int, event_type: str) -> Sequence:
        # 9. Find all teams that participated in a year and event_type (e.g., winter 2016).
        statement = (
            select(Team.name)
            .join(Team, Games.teams)
            .where(Games.event_type == event_type and Games.year == year)
        )
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def query_games_disability(self, disability: str) -> Sequence:
        # 10. Find all the Paralympics that have competitors who are 'Amputees'
        statement = (
            select(Games.year, Games.event_type, Disability.description)
            .join(Disability, Games.disabilities)
            .where(Disability.description == disability)
        )
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results

    def update_disability(self, disability_description: str) -> Disability:
        # 11. **Update** all instances of the disability 'Les Autres' to 'Other'
        with Session(self.engine) as session:
            # Find the disabiity
            statement = select("complete this!")
            disability = session.exec(statement).one()
            # Make the change to disability.description
            disability.description = disability_description
            # Commit
            session.commit()
            # Refresh
            session.refresh(disability)
            return disability
