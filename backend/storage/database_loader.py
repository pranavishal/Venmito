import sqlite3
import pandas as pd
from pathlib import Path
import os

# Paths
DB_PATH = Path("storage/venmito.db")
CLEANED_DATA_PATH = Path("datasets/processed/")

# Deletes existing database if it exists
def delete_existing_database(db_path):
    """Delete the existing database file if it exists"""
    try:
        if db_path.exists():
            os.remove(db_path)
            print(f"Existing database {db_path} has been deleted.")
        else:
            print(f"No existing database found at {db_path}")
    except Exception as e:
        print(f"Error deleting existing database: {e}")

# Connect to the database
def connect_to_database(db_path):
    try:
        connection = sqlite3.connect(db_path)
        print(f"Connected to database at {db_path}")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Create tables in the database
def create_tables(connection, schema_path):
    try:
        with open(schema_path, "r") as file:
            schema = file.read()
        cursor = connection.cursor()
        cursor.executescript(schema)
        connection.commit()
        print("Database schema created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Load data from CSV file into a table
def load_data_to_table(connection, table_name, csv_file):
    try:
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, connection, if_exists="append", index=False)
        print(f"Data from {csv_file} loaded into {table_name} table successfully.")
    except Exception as e:
        print(f"Error loading data into {table_name}: {e}")

# Main function to setup the database and load data
if __name__ == "__main__":
    # Delete existing database first
    delete_existing_database(DB_PATH)

    # Connect to (or create) the database
    connection = connect_to_database(DB_PATH)
    if connection is None:
        exit()

    # Create tables
    schema_path = Path("storage/database_schema.sql")
    create_tables(connection, schema_path)

    # Define table and CSV mappings
    table_csv_mapping = {
        "People": CLEANED_DATA_PATH / "people_merged.csv",
        "Promotions": CLEANED_DATA_PATH / "promotions_cleaned.csv",
        "Transactions": CLEANED_DATA_PATH / "transactions_cleaned.csv",
        "Transfers": CLEANED_DATA_PATH / "transfers_cleaned.csv",
    }

    # Load data into tables
    for table_name, csv_file in table_csv_mapping.items():
        load_data_to_table(connection, table_name, csv_file)

    # Close the connection
    connection.close()
    print("Database setup and data loading completed!")