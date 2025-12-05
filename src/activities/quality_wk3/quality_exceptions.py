import sqlite3


def create_db(schema_path, db_path):
    """ Create a SQLite database using the provided schema file.

    Args:
        schema_path (str): Path to the SQL schema file.
        db_path (str): Path where the SQLite database will be created.
    """
    conn = None
    try:
        # Create a connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Read the SQL schema file
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        # Execute the schema SQL
        cursor.executescript(schema_sql)

        # Commit the changes
        conn.commit()
    except (sqlite3.Error, OSError) as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        if conn:
            conn.close()