""" Creates the database file with tables """
from importlib import resources

import pandas as pd
from sqlmodel import SQLModel, Session, create_engine, delete, select

from para_app import data
from para_app.models import Country, Disability, Games, GamesDisability, GamesHost, GamesTeam, Host, Team  # noqa

db_file = resources.files(data).joinpath("paralympics.db")
db_url = f"sqlite:///{str(db_file)}"

engine = create_engine(
    db_url,
    echo=False
)  # Echo=True prints the SQL to the terminal, which can help when debugging.


def create_db_and_tables():
    """ Created the database file and tables if they do not already exist.

    Note: this does not pick up on changes to existing tables. Hint for extended learning: Alembic for migrations

    """
    SQLModel.metadata.create_all(engine)


def drop_data(engine):
    """ Drops the data from all the tables."""

    # Delete in dependency order: child tables first, then parents
    delete_order = [
        GamesDisability,
        GamesHost,
        GamesTeam,
        Host,
        Games,
        Team,
        Country,
        Disability,
    ]

    with Session(engine) as session:
        for model in delete_order:
            session.exec(delete(model))
        session.commit()


def add_data(engine):
    """ Adds data to the database from the .xslx file

    This is adapted from the original code to add data.
    To be replaced with the crud_service.

    For reference, column names from the excel sheets:

    df_games_cols = ['type', 'year', 'country', 'host', 'start', 'end',
                     'disabilities_included', 'countries', 'events', 'sports',
                     'participants_m', 'participants_f', 'participants', 'highlights',
                     'URL']
    df_teams_cols = ['Code', 'TeamName', 'Region', 'SubRegion', 'MemberType', 'Notes']
    """

    data_file = resources.files(data).joinpath("paralympics_all_raw.xlsx")

    # Read games and teams sheets keeping NaNs for controlled conversion
    df_games = pd.read_excel(data_file, sheet_name="games", keep_default_na=True)
    df_teams = pd.read_excel(data_file, sheet_name="team_codes", keep_default_na=True)

    # Convert integer-like columns to nullable Int64
    games_int_cols = ['year', 'participants_m', 'participants_f', 'participants', 'events', 'sports', 'countries']
    for col in games_int_cols:
        if col in df_games.columns:
            df_games[col] = pd.to_numeric(df_games[col], errors='coerce').astype('Int64')

    # Convert date-like columns to strings in dd-mm-YYYY format
    for col in df_games.columns:
        if col.lower() in ('start', 'end') or 'date' in col.lower():
            df_games[col] = pd.to_datetime(df_games[col], errors='coerce').dt.strftime('%d-%m-%Y')

    # Disabilities
    # Collect unique disability values (split comma-separated strings into individual values)
    df_disability = (
        df_games['disabilities_included']
        .dropna()
        .astype(str)
        .str.split(',')
        .explode()
        .str.strip()
    )
    df_disability = df_disability[df_disability != ''].unique().tolist()
    with Session(engine) as session:
        for d in df_disability:
            dis = Disability(description=d)
            session.add(dis)
        session.commit()

    # Countries and Teams
    # For every row, if df_teams['MemberType'] = "country" then save that value to Country and add the id of the
    # inserted Country as the foreign key to create a Team.
    # If df_team['MemberType'] is not "country", then just add a Team without the FK
    for _, row in df_teams.iterrows():
        # Normalize values from the row
        code = str(row.get('Code')).upper()  # 3-letter code in uppercase
        member_type = str(row.get('MemberType', '')).strip().lower()
        team_name = row.get('TeamName').strip()
        region = row.get('Region') if 'Region' in row else None
        notes = row.get('Notes') if 'Notes' in row else None

        with Session(engine) as session:
            country_id = None

            # For any that is member_type of country then get the country id
            if not pd.isna(team_name) or team_name != '':
                if member_type == 'country':
                    # Find or create the Country and get its id
                    statement = select(Country).filter(Country.country_name == team_name)
                    country = session.exec(statement).first()
                    if not country:
                        country = Country(country_name=team_name)
                        session.add(country)
                        session.commit()
                        session.refresh(country)
                    country_id = country.id

            # Create the Team, linking to country_id when applicable
            team = Team(
                code=code,
                name=str(team_name).strip(),
                region=region,
                notes=notes,
                member_type=member_type,
                country_id=country_id
            )
            session.add(team)
            session.commit()

    # Host
    with Session(engine) as session:
        host_objs = []
        for _, row in df_games.iterrows():
            # Normalize and replace common country short names before lookup
            country_name = row.get('country')
            if pd.isna(country_name):
                continue
            country_name = str(country_name).strip()
            replacements = {
                "USA": "United States of America",
                "UK": "Great Britain",
                "China": "People's Republic of China",
                "Korea": "Republic of Korea",
                "Russia": "Russian Federation",
            }
            lookup_country = replacements.get(country_name, country_name)
            statement = select(Country).filter(Country.country_name == lookup_country)
            country = session.exec(statement).first()

            if not country:
                # print(f"{row['country']} not found in database")
                continue

            host_val = row.get('host')
            if pd.isna(host_val):
                continue

            host_str = str(host_val)
            # Split on comma into multiple host names, strip whitespace, ignore empty entries
            host_names = [h.strip() for h in host_str.split(',') if h.strip()]
            for host_name in host_names:
                # Skip empty host names
                if not host_name:
                    continue
                h = Host(place_name=host_name, country_id=country.id)
                host_objs.append(h)
        if host_objs:
            seen = set()
            unique_hosts = []
            for h in host_objs:
                key = (h.place_name, h.country_id)
                if key not in seen:
                    seen.add(key)
                    unique_hosts.append(h)
            session.add_all(unique_hosts)
            session.commit()

        # Special-case rows where multiple countries are listed (e.g. "UK, USA") and hosts align by position.
        mask = df_games['country'].astype(str).str.strip() == 'UK, USA'
        row = df_games.loc[mask].head(1)
        country_field = row.get('country')
        host_field = row.get('host')

        if ',' in str(country_field) and ',' in str(host_field):
            country_parts = [c.strip() for c in str(country_field).split(',') if c.strip()]
            host_parts = [h.strip() for h in str(host_field).split(',') if h.strip()]
            # Pair up by position; ignore extras
            for c_name, h_name in zip(country_parts, host_parts):
                lookup_country = replacements.get(c_name, c_name)
                stmt = select(Country).filter(Country.country_name == lookup_country)
                country_obj = session.exec(stmt).first()
                if not country_obj:
                    continue
                host_stmt = select(Host).filter(Host.place_name == h_name, Host.country_id == country_obj.id)
                if session.exec(host_stmt).first():
                    continue
                host_objs.append(Host(place_name=h_name, country_id=country_obj.id))

    # Games, GamesDisability, GamesHost, GamesTeam
    with Session(engine) as session:
        for _, row in df_games.iterrows():
            # Convert NaN or NA to None
            def san(v):
                return None if pd.isna(v) else v

            g = Games(
                event_type=row.get('type').strip().lower(),
                year=row.get('year'),
                start_date=san(row.get('start')),
                end_date=san(row.get('end')),
                countries=san(row.get('countries')),
                events=san(row.get('events')),
                sports=san(row.get('sports')),
                participants_m=san(row.get('participants_m')),
                participants_f=san(row.get('participants_f')),
                participants=san(row.get('participants')),
                highlights=san(row.get('highlights')),
                url=san(row.get('URL'))
            )
            session.add(g)
            session.commit()
            session.refresh(g)
            games_id = g.id

            # GamesTeam
            # Find the Team.id where row.get('country') matches Team.name, create and add GamesTeam(games_id=games_id, team_id=Team.id)
            country_name = row.get('country')
            if not pd.isna(country_name):
                statement = select(Team).filter(Team.name == country_name)
                team = session.exec(statement).first()
                if team:
                    games_team = GamesTeam(games_id=games_id, team_id=team.code)
                    session.add(games_team)
                    session.commit()

            # GamesDisability
            # Get row.get('disabilities_included') and split on the comma into a list of strings. For each string, find
            # the Disability.id where Disability.description matches the string, and insert
            # GamesDisability(games_id=games_id, disability_id=disability_id)
            dis_val = row.get('disabilities_included')
            if not pd.isna(dis_val):
                dis_list = [d.strip() for d in str(dis_val).split(',') if d.strip()]
                games_dis_objs = []
                for dis_desc in dis_list:
                    statement = select(Disability).filter(Disability.description == dis_desc)
                    disability = session.exec(statement).first()
                    if disability:
                        games_dis_objs.append(GamesDisability(games_id=games_id, disability_id=disability.id))
                    else:
                        # Create missing Disability record (safe fallback)
                        new_dis = Disability(description=dis_desc)
                        session.add(new_dis)
                        session.commit()
                        session.refresh(new_dis)
                        games_dis_objs.append(GamesDisability(games_id=games_id, disability_id=new_dis.id))
                if games_dis_objs:
                    session.add_all(games_dis_objs)
                    session.commit()

            # GamesHost
            # Find the Host.host_id where row.get('host') matches Host.place_name, then use games_id and host_id to
            # insert GamesHost. Where row.get('host') has multiple strings separated by a comma, then create one
            # GamesHost row for each pair of host_id and games_id
            host_val = row.get('host')
            if not pd.isna(host_val):
                host_names = [h.strip() for h in str(host_val).split(',') if h.strip()]
                games_host_objs = []
                for host_name in host_names:
                    statement = select(Host).filter(Host.place_name == host_name)
                    host = session.exec(statement).first()
                    if not host:
                        # Try to link host to the game's country when possible
                        country_name = row.get('country')
                        country_id = None
                        if not pd.isna(country_name):
                            country_stmt = select(Country).filter(Country.country_name == country_name)
                            country = session.exec(country_stmt).first()
                            if country:
                                country_id = country.id
                        host = Host(place_name=host_name, country_id=country_id)
                        session.add(host)
                        session.commit()
                        session.refresh(host)
                    games_host_objs.append(GamesHost(games_id=games_id, host_id=host.id))
                if games_host_objs:
                    session.add_all(games_host_objs)
                    session.commit()
