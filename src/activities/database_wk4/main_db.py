from importlib import resources

import pandas as pd

from activities import data, starter
from activities.database_wk3.solutions_db import create_db
from activities.database_wk3.solutions_extra_db import insert_data


def main():
    """ Main for the core week 3 database activities """
    # Activity 3.03 Describe the data for the database design activity
    # path_para_raw = resources.files(data).joinpath("paralympics_all_raw.xlsx")
    # df_games, df_codes = read_data_to_df(path_para_raw)
    # describe(df_games, df_codes)

    # Activity 3.11 Create the database
    # db_path = resources.files(data_solutions).joinpath("paralympics.db")
    # schema_path = resources.files(data_solutions).joinpath("paralympics_schema.sql")
    db_path = resources.files(data).joinpath("sample.db")
    schema_path = resources.files(starter).joinpath("student_schema.sql")
    create_db(schema_path, db_path)


def extra():
    """ Main for the extra activities. These are optional. """

    db_path = resources.files(data).joinpath("student.sqlite")
    data_path = resources.files(data).joinpath("student_data.csv")

    # Create the student database if you don't have it
    # schema_path = resources.files(starter).joinpath("student_schema.sql")
    # create_db(schema_path=schema_path, db_path=db_path)

    # Insert data
    df = pd.read_csv(data_path)
    # delete_rows(db_path)  # removes data from all tables, you need to do this if you want to run insert more than once
    insert_data(db_path, df)


if __name__ == '__main__':
    main()
    # extra()
