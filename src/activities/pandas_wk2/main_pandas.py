""" Main to run the week 2 (pandas) worked solutions. """
import sys
from importlib import resources
from pathlib import Path

import pandas as pd

from activities import data
from activities.pandas_wk2.solutions_pandas import Demonstrate, describe, explore_event_data, prepare_event_data


def main():
    path_para_raw = resources.files(data).joinpath("paralympics_raw.csv")
    # Read the data from the file into a Pandas dataframe
    # Activity 2.10: read selected columns
    # cols = ['type', 'year', 'country', 'host', 'start', 'end', 'countries', 'events', 'sports',
    #        'participants_m', 'participants_f', 'participants']

    # df_selected_cols = pd.read_csv(path_para_raw, usecols=cols)

    events_csv_df = pd.read_csv(str(path_para_raw))

    # Temporarily redirect the output from the terminal to a file
    original_stdout = sys.stdout

    # Check output directory created
    output_dir = Path(__file__).parent.joinpath("output")
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Describe
    describe_txt = Path(__file__).parent.joinpath("output", "df_describe.txt")
    with open(describe_txt, "w") as f:
        sys.stdout = f
        # Call the function named 'describe' - you may have a different function name
        describe(events_csv_df)

    # Explore
    explore_txt = Path(__file__).parent.joinpath("output", "df_explore.txt")
    with open(explore_txt, "w") as f:
        sys.stdout = f
        # Call the function named 'explore' - you may have a different function name
        explore_event_data(events_csv_df)

    # Prepare
    prepare_txt = Path(__file__).parent.joinpath("output", "df_prepare.txt")
    with open(prepare_txt, "w") as f:
        sys.stdout = f
        df_prepared = prepare_event_data(events_csv_df)

    # Run describe again on the prepared dataset
    describe_after_txt = Path(__file__).parent.joinpath("output", "df_describe_after.txt")
    with open(describe_after_txt, "w") as f:
        sys.stdout = f
        describe(df_prepared)

    # Check if the data is sufficient for the purpose
    check_txt = Path(__file__).parent.joinpath("output", "df_check_sufficient.txt")
    with open(check_txt, "w") as f:
        sys.stdout = f

        # Created as a class just to show a different approach, no need to create a class
        demonstrate = Demonstrate(df_prepared)
        demonstrate.where()
        demonstrate.when_events()
        demonstrate.change_over_time('events')
        demonstrate.change_over_time('sports')

    # Restore stdout from file to terminal
    sys.stdout = original_stdout


if __name__ == "__main__":
    main()
