""" Mimics a typical file structure when using models classes and database witin an app

See https://sqlmodel.tiangolo.com/tutorial/code-structure/
There is no actual app code yet though!
"""
from activities.database2_wk8.database import create_db_and_tables, drop_db_and_tables
from activities.database2_wk8.queries import select_queries, update_queries, add_all_data


def main():
    # drop_db_and_tables()
    # create_db_and_tables()
    # add_all_data()
    # select_queries()
    update_queries()


if __name__ == '__main__':
    main()
