from importlib import resources

import matplotlib.pyplot as plt
import pandas as pd

from activities import data


def describe(df: pd.DataFrame):
    """Uses pandas DataFrame functions to describe the data.

    Applies the following pandas functions to the DataFrame and prints the output to file instead of terminal:
        df.shape
        dd.head(num)
        df.tail(num)
        df.columns
        df.dtypes
        df.describe()
        df.info()

       Args:
       df (Pandas DataFrame): Pandas DataFrame with the data

    """
    # 2.3 Describe
    pd.set_option("display.max_columns", None)  # Change the pandas display options to print all columns
    print("\nThe number of rows and columns\n", df.shape)
    print("\nThe first 5 rows\n", df.head(5))
    print("\nThe last 5 rows\n", df.tail(5))
    print("\nThe column labels\n", df.columns)
    print("\nThe column datatypes\n", df.dtypes)
    print("\nInfo\n", df.info())
    print("\nDescribe\n", df.describe())


def explore_event_data(df: pd.DataFrame):
    """ Explores the data contents of the events data

    It does so by considering the contents of each column in the dataset and looks at:

        - distribution of values
        - outliers
        - missing values
        - categorical values

    TODO: Consider restructuring into smaller functions

    Args:
        df (object): pandas DataFrame with the raw data
    """
    # 2.4 Missing values
    print("\nNumber of missing values in the DataFrame:\n", df.isna().sum().sum())

    missing_rows = df[df.isna().any(axis=1)]
    print("\nOnly the rows with missing values:\n", missing_rows)

    missing_columns = df.loc[:, df.isna().any(axis=0)]
    print("\nOnly the columns with missing values:\n", missing_columns)

    # 2.6 Histograms to view distribution of values
    # Histogram of any columns with values of a data type that can be plotted
    df.hist(
        sharey=False,  # defines whether y-axes will be shared among subplots.
        figsize=(12, 8)  # a tuple (width, height) in inches
    )
    plt.savefig("output/histogram_df.png")

    # Histograms of specific columns only
    df[["participants_m", "participants_f"]].hist()
    plt.savefig("output/histogram_participants.png")

    # Histograms based on filtered values
    summer_df = df[df['type'] == 'summer']
    summer_df.hist(sharey=False, figsize=(12, 8))
    plt.savefig("output/histogram_summer.png")

    # 2.6 part 2: Box plots to consider outliers
    # Box plots to explore range and consider potential outliers
    df.boxplot()
    plt.savefig("output/boxplot_all.png")

    # Generate a subplot for the sports column.
    # TODO: Modify the axes to show integers only.
    df[["sports"]].boxplot()
    plt.savefig("output/boxplot_sports.png")

    # Generate subplots for each column, each with its own y-axis
    df.plot(subplots=True, kind="box", sharey=False, figsize=(16, 6))
    plt.tight_layout()
    plt.savefig("output/boxplot_subplots.png")

    # 2.7 Timeseries data
    df.plot(x="start", y="participants")
    plt.xticks(rotation=90)  # Rotate x-axis labels by 90 degrees
    plt.savefig("output/timeseries.png")

    df.groupby("type").plot(x="start", y="participants")
    plt.savefig("output/timeseries_grouped.png")

    # 2.8 Print categorical values
    print("\nDistinct categorical values in the event 'type' column\n", df['type'].unique())
    print("\nCount of each distinct categorical value in the event 'type' column\n", df['type'].value_counts())
    print("\nDistinct categorical values in the event 'disabilities_included' column\n",
          df['disabilities_included'].unique())
    print("\nCount of each distinct categorical value in the event 'type' column\n",
          df['disabilities_included'].value_counts())


def prepare_event_data(df: pd.DataFrame):
    """ Prepares the event data based on the activities

    2.11 Drop columns
    2.12 Address missing values
    2.12 Correct incorrect values
    2.13 Change float to integer data type
    2.13 Change string (object) to date

    Args:
        df (pd.DataFrame): pandas DataFrame with the raw data

    Returns:
        df (pd.DataFrame): pandas DataFrame with the data after changes are made

    """
    # 2.11 Drop columns
    cols_to_drop = ['URL', 'disabilities_included', 'highlights']
    df_dropped = df.drop(columns=cols_to_drop)
    print("\nColumns after dropping:\n", df_dropped.columns)
    # Re-assigning the dataframe name for ease of reference in the subsequent code
    df = df_dropped

    # 2.12 Address missing values
    missing_rows = df[df.isna().any(axis=1)]
    print("\nRows with missing values after columns dropped:\n", missing_rows)

    # 2.12 Correct incorrect values
    print("\nDistinct categorical values in the event 'type' column before change\n", df['type'].unique())
    # Change 'Summer' to 'summer'
    event_type = "Summer"
    df.loc[df.query("type == @event_type").index, 'type'] = 'summer'
    # Removes leading and trailing whitespace from all values in the 'type' column
    df['type'] = df['type'].str.strip()
    print("\nDistinct categorical values in the event 'type' column after changes\n", df['type'].unique())

    # 2.13 Change float64 and int64 to Int64 data type
    print("\nData types:\n", df.dtypes)
    columns_to_change = ['countries', 'events', 'participants_m', 'participants_f', 'participants', 'sports', 'year']
    for col in columns_to_change:
        df[col] = df[col].astype('Int64')

    # 2.13 Change object (strings) to date
    print("\nValues in start and end before change: \n", df[['start', 'end']])
    df['start'] = pd.to_datetime(df['start'], format='%d/%m/%Y')
    df['end'] = pd.to_datetime(df['end'], format='%d/%m/%Y')
    print("\nData types after float to int and string to date changes:\n", df.dtypes)

    # 2.13 Optional: change object to string
    cols = ['type', 'country', 'host']
    for col in cols:
        df[col] = df[col].astype('string')
    print("\nData types after object to string to date changes:\n", df.dtypes)

    # 2.14 Add new column
    # This should work as the dates have been converted to date format.
    duration_values = (df['end'] - df['start']).dt.days.astype('Int64')
    df.insert(df.columns.get_loc('end') + 1, 'duration', duration_values)
    print("\nNew duration column:\n", df['duration'])
    print("\nAll columns after adding duration:\n", df.columns)

    # 2.15 Add Code column by merging the Code and Name from npc_codes
    # Ensure the values match in the merge column
    replacement_names = {
        'UK': 'Great Britain',
        'USA': 'United States of America',
        'Korea': 'Republic of Korea',
        'Russia': 'Russian Federation',
        'China': "People's Republic of China"
    }
    df['country'] = df['country'].replace(replacement_names)

    path_npc = resources.files(data).joinpath("npc_codes.csv")
    npc_df = pd.read_csv(path_npc, encoding='utf-8', encoding_errors='ignore', usecols=['Code', 'Name'])
    merged_df = df.merge(npc_df, how='left', left_on='country', right_on='Name')
    # Find the rows where the country and Name were not matched, these will be NaNs
    missing_rows = merged_df[['country', 'Code', 'Name']][merged_df[['country', 'Code', 'Name']].isna().any(axis=1)]
    print("\nOnly the rows with missing values:\n", missing_rows)

    df = merged_df.drop(columns=['Name'])
    print("\nFinal dataframe contents:\n", df)

    # 2.16 Save to file
    # Note the data types are not saved, .csv is comma separated text values
    path_prepared = resources.files(data).joinpath("paralympics_prepared.csv")
    df.to_csv(path_prepared, encoding='utf-8', index=False)

    # Return the dataframe so it can be used by other functions
    return df


# Written as a class just to show an example of a class instead of a function.
# This does not imply a class is better nor is it necessary!
# Classes are covered in a later week for those not familiar with classes.
class Demonstrate:
    """ Class with methods to check if the prepared event data is sufficient for the purpose

    Data to be used by high school students to answer questions:

    1. Where in the world have paralympic events have been held?
    2. When have the events been held? (dates)
    3. How have the number of sports and events included changed over time?
    4. What are the trends in participant numbers over time? How does this vary by gender? How does this vary by winter and summer events?

    Attributes:
        df (pd.DataFrame): The prepared DataFrame containing event data.
     """

    def __init__(self, df: pd.DataFrame):
        """ Initializes the Demonstrate class with the provided DataFrame.

        Args:
            df (pd.DataFrame): The prepared DataFrame containing event data.
        """
        self.df = df

    def where(self):
        """ Prints a unique pairs of host + country and is sorted by country

        Purpose is to check if there is data to answer the question:
            Where in the world have paralympic events have been held?
        """
        unique_pairs = self.df[['host', 'country']].drop_duplicates().sort_values(by='country')
        print("\nWhere in the world have paralympic events have been held?\n",
              unique_pairs[['country', 'host']].to_string(index=False))

    def when_events(self):
        """ Prints a list of when the paralympic games have been held,
        including start and end dates, host, and year. Ordered by start date.

        Purpose is to check if there is data to answer the question:
            When have the paralympic games been held?
        """
        df_table = self.df[['start', 'end', 'host', 'year']]
        df_table = df_table.sort_values(by='start')
        print("\nWhen have the events been held?\n", df_table.to_string(index=False))

    def change_over_time(self, column_name):
        """ Generates a line chart to show how a column's values vary over time.

        Uses the start date.

        Args:
            column_name (str): The name of the column, e.g. 'events', 'sports'
        """
        # select the columns of interest, order by start date and reset the index
        df_plt = self.df[['type', 'start', column_name]].sort_values(by='start').reset_index(drop=True)
        print(df_plt.head())

        # Winter and summer together
        df_plt.plot(x='start', y=column_name)
        plt.savefig('output/winter-summer-combined-' + column_name + '.png')

        # Separate charts for winter and summer
        winter_df = df_plt.query("type == 'winter'")
        winter_df.plot(x='start', y=column_name, title='Winter paralympics - ' + column_name)
        plt.savefig('output/winter-' + column_name + '.png')

        summer_df = df_plt.query("type == 'summer'")
        summer_df.plot(x='start', y=column_name, title='Summer paralympics - ' + column_name)
        plt.savefig('output/summer-' + column_name + '.png')
