"""
Database Utility Module
-----------------------
Provides reusable functions for connecting to PostgreSQL,
reading tables into pandas DataFrames, and writing DataFrames
back to PostgreSQL.
"""

import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ==========================
# Load Environment Variables
# ==========================
load_dotenv()


# ==========================
# Create Database Engine
# ==========================
def get_engine():
    """
    Creates and returns a SQLAlchemy engine.
    """

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    connection_string = (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    return create_engine(connection_string)


# ==========================
# Read Table
# ==========================
def read_table(schema, table_name):
    """
    Reads a PostgreSQL table into a pandas DataFrame.
    """

    engine = get_engine()

    query = f"SELECT * FROM {schema}.{table_name}"

    return pd.read_sql(query, engine)


# ==========================
# Write Table
# ==========================
def write_table(df, schema, table_name, if_exists="replace"):
    """
    Writes a DataFrame to PostgreSQL.
    """

    engine = get_engine()

    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists=if_exists,
        index=False
    )

    print(f"✅ Table written: {schema}.{table_name}")


# ==========================
# Test Connection
# ==========================
def test_connection():
    """
    Tests whether PostgreSQL is reachable.
    """

    engine = get_engine()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("✅ PostgreSQL connection successful!")


# ==========================
# Run Only When Executed Directly
# ==========================
if __name__ == "__main__":
    test_connection()