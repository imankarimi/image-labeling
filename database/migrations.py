import os
import sqlite3


class Migration:
    def __init__(self):
        # Create a database or connect to an existing one
        database_path = os.path.realpath('database/image_labeling.db')
        self.db_connection = sqlite3.connect(database_path)
        self.db_cursor = self.db_connection.cursor()

    def run(self):
        # Create tables
        file_path_tb = "CREATE TABLE IF NOT EXISTS setting_file_path (id INTEGER PRIMARY KEY,file_path TEXT)"
        labels_tb = "CREATE TABLE IF NOT EXISTS setting_labels (id INTEGER PRIMARY KEY,code INT,name TEXT,color_code TEXT)"

        # Create a table if it doesn't exist
        self.db_cursor.execute(file_path_tb)
        self.db_cursor.execute(labels_tb)
        self.db_connection.commit()
        # self.db_connection.close()

    def clean(self):
        # Query to find all tables
        self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.db_cursor.fetchall()

        # Iterate through all tables and delete data from each one
        for table in tables:
            try:
                self.db_cursor.execute(f"DELETE FROM {table[0]};")
                print(f"Data from table {table[0]} has been deleted.")
            except sqlite3.OperationalError as e:
                print(f"Could not delete data from {table[0]}: {e}")

        # Commit the changes and close the connection
        self.db_connection.commit()
        self.db_connection.close()

    def reset(self):
        # Query to find all tables
        self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.db_cursor.fetchall()

        # Iterate through all tables and drop each one
        for table in tables:
            try:
                self.db_cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
                print(f"Table {table[0]} has been dropped.")
            except sqlite3.OperationalError as e:
                print(f"Could not drop table {table[0]}: {e}")

        # Commit the changes and close the connection
        self.db_connection.commit()
        self.db_connection.close()
