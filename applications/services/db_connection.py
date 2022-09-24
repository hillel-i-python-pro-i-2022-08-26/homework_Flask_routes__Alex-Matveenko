import sqlite3

from applications.settings import db_path


# Create_connection_to_database__start
class Dbconnection:

    def __init__(self):
        self._connection: sqlite3.Connection | None = None

    # Connect_to_database
    def __enter__(self):
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    # Close_connection_to_database
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

# Create_connection_to_database__stop