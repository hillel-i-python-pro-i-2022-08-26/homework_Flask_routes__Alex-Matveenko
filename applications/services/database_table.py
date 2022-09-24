from applications.services.db_connection import Dbconnection


# Create_database_table__start
def create_table():
    with Dbconnection() as connection:
        with connection:
            connection.execute("""
            CREATE TABLE IF NOT EXISTS phones (
            phoneID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            contact_name VARCHAR NOT NULL,
            phone_value INTEGER NOT NULL
            )
            """)

# Create_database_table__start
