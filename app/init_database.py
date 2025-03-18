# init_database.py

import os
import sqlite3

def init_database(db_path, sql_files):
    """
    Initializes the database by executing SQL commands from multiple files.
    :param db_path: Path to the SQLite database file.
    :param sql_files: List of relative paths to the SQL files containing initialization commands.
    """
    # Resolve the absolute path to the database file
    db_path = os.path.normpath(os.path.join(os.path.dirname(__file__), db_path))
    print(f"Database path: {db_path}")

    # Ensure the database file exists (or create it if it doesn't)
    if not os.path.exists(db_path):
        print(f"Creating new database file at: {db_path}")
        open(db_path, 'w').close()  # Create an empty file

    # Process each SQL file
    for sql_file in sql_files:
        # Resolve the absolute path to the SQL file
        resolved_sql_path = os.path.normpath(os.path.join(os.path.dirname(__file__), sql_file))
        print(f"Initializing database from SQL file: {resolved_sql_path}")

        # Check if the SQL file exists
        if not os.path.exists(resolved_sql_path):
            raise FileNotFoundError(f"SQL file not found at: {resolved_sql_path}")

        # Read and execute the SQL commands with UTF-8 encoding
        try:
            with open(resolved_sql_path, 'r', encoding='utf-8') as f:
                sql_commands = f.read()

            # Connect to the database and execute the commands
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.executescript(sql_commands)  # Executes multiple SQL statements
                conn.commit()

            print(f"Database initialized successfully from: {resolved_sql_path}")
        except Exception as e:
            print(f"Error initializing database from: {resolved_sql_path} | Error: {e}")

if __name__ == "__main__":
    # Define the database file and SQL files to initialize the database
    DATABASE_PATH = "database/jokes.db"
    SQL_FILES = [
        "database/jokes.schema.sql",  # Schema file (must come first)
        "database/jokes.ar.sql",      # Arabic jokes
        "database/jokes.en.sql",      # English jokes
        # Add more language files here as needed
    ]

    # Initialize the database
    init_database(DATABASE_PATH, SQL_FILES)