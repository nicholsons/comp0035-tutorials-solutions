""" Worked solutions for the optional extra activities in 3_database """
import sqlite3
from importlib import resources

import pandas as pd

from activities import data


def delete_rows(db_path, table_names=None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if not table_names:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        table_names = [row[0] for row in cur.fetchall()]
    for table_name in table_names:
        cur.execute(f"DELETE FROM {table_name}")
    conn.commit()
    conn.close()


def insert_data(db_path, df):
    """ Insert student, teacher and course data into the database

    Args:
        db_path (str): Path where the SQLite database will be created.
        df (pandas.DataFrame): Student data from the csv file.
    """
    # Create a connection to the database using sqlite3
    connection = sqlite3.connect(db_path)

    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()

    # Enable foreign key constraints for sqlite
    # By default, foreign key constraints are disabled in SQLite, enable them explicitly for each database connection.
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Define the SQL insert statements for the parameterised queries
    test_sql = 'INSERT INTO student (...) VALUES (?, ?)'
    student_sql = 'INSERT INTO student (student_name, student_email) VALUES (?, ?)'
    teacher_sql = 'INSERT INTO teacher (teacher_name, teacher_email) VALUES (?, ?)'
    course_sql = 'INSERT INTO course (course_name, course_code, course_schedule, course_location) VALUES (?, ?, ?, ?)'

    # Create dataframe with the unique values for the columns needed for the student table (excluding the student_id PK)
    student_df = pd.DataFrame(df[['student_name', 'student_email']].drop_duplicates())
    teacher_df = pd.DataFrame(df[['teacher_name', 'teacher_email']].drop_duplicates())
    course_df = pd.DataFrame(df[['course_name', 'course_code', 'course_schedule', 'course_location']].drop_duplicates())

    # Get the values as a list rather than pandas Series. The parameterised query expects a list.
    student_data = student_df.values.tolist()
    teacher_data = teacher_df.values.tolist()
    course_data = course_df.values.tolist()

    # Use `executemany()` with a parameterised query to add the values to the table.
    cursor.executemany(student_sql, student_data)
    cursor.executemany(teacher_sql, teacher_data)
    cursor.executemany(course_sql, course_data)

    # Insert data for the enrollment table
    enrollment_insert_sql = """
                            INSERT INTO enrollment (student_id, course_id, teacher_id)
                            VALUES ((SELECT student_id FROM student WHERE student_email = ?), \
                                    (SELECT course_id FROM course WHERE course_name = ? AND course_code = ?), \
                                    (SELECT teacher_id FROM teacher WHERE teacher_email = ?)) \
                            """
    for _, row in df.iterrows():
        cursor.execute(
            enrollment_insert_sql,
            (
                row['student_email'],
                row['course_name'],
                row['course_code'],
                row['teacher_email'],
            )
        )

    # Commit the changes to the database
    connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()


def example_select_queries(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Select all rows and columns from the student table
    cur.execute('SELECT * FROM student')
    rows = cur.fetchall()  # Fetches more than 1 row
    print("\nAll rows and columns from the student table\n")
    for row in rows:
        print(row)

    # Select the student_id column
    cur.execute("SELECT student_id FROM student WHERE student_name = 'Alice Brown'")
    row = cur.fetchone()  # Fetches the first result
    print("\nSelect the student_id: \n", row[0])

    cur.execute("SELECT teacher_name, teacher_email FROM teacher WHERE teacher_id in (1, 2)")
    rows = cur.fetchall()  # Fetches all rows from the result
    print("\nTeacher name and email where the teacher is id 1 or 2\n")
    for row in rows:
        print(row)

    con.close()


def create_unnormalised_db(df):
    """ Creates single table database from the paralympics data.

     Used for activity 3.17
     """
    db_para_path = resources.files(data).joinpath("para-not-normalised.sqlite")
    data_path_para = resources.files(data).joinpath("paralympics_all_raw.xlsx")
    connection = sqlite3.connect(db_para_path)
    df = pd.read_excel(str(data_path_para))
    df.to_sql("Games", connection, if_exists="replace")
    connection.close()
