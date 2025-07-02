"""Reusable utility functions for CryptoPredictor"""

import pandas as pd
import psycopg2
from pathlib import Path
from contextlib import (
    contextmanager,
)  # Decorator to write custom context managers using generator functions instead of classes
from config.config import DB_CONFIG, DB_API_CONFIG
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowFailException
from typing import Optional
from psycopg2 import Error as PsycopgError


def ensure_directory(path: str | Path):
    """Create directory if it doesn't exist."""
    try:
        dir_path = Path(path) if not isinstance(path, Path) else path
        print(f"Ensuring directory: {dir_path}")
        if not dir_path.exists():
            print(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            print(f"Directory already exists: {dir_path}")
    except Exception as e:
        print(f"Error creating directory {dir_path}")
        raise


def validate_dataframe(df: pd.DataFrame, expected_columns: list):
    """Validate DataFrame structure it ensure the data
      is correct extracted base on our requirements"""
    if df.empty:
        raise ValueError("DataFrame is empty")
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")


@contextmanager
def get_db_connection(config: dict):
    """Context manager for PostgreSQL connections.
    Establishes a DB connection and yields it.
    The connection is automatically closed when the block exits."""
    conn = None
    try:
        conn = psycopg2.connect(**config)
        yield conn
        # It is used to used to return object temporarily
        # to caller and pause untill caller is done
    finally:
        if conn:
            conn.close()


# Trucated table is more faster than deleting the table
# because it remove complete data srcipt one time from data table
# without removing the table structure
def truncate_table(table_name: str):
    """Deletes all data from a table"""
    try:
        hook = PostgresHook(postgres_conn_id="my_postgres_conn_id")
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
        conn.commit()
        print(f"Truncate table {table_name} sucessfully")
    except Exception as e:
        print(f"Failed to trucate table {table_name}: {str(e)}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_table(create_query):
    """Creates the table if not exists and
    ensures the unique constraint is applied"""
    try:
        hook = PostgresHook(postgres_conn_id="my_postgres_conn_id")
        conn = hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(create_query)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise AirflowFailException(
            f"Failed to create table or add constraint: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def is_new_data(coin: str, table_name: str) -> Optional[datetime]:
    try:
        with get_db_connection(DB_CONFIG) as conn:
            df = pd.read_sql(
                f"SELECT * FROM {table_name} ORDER BY date DESC LIMIT 1", conn
            )

            if df.empty:
                return None

            return pd.to_datetime(df.iloc[0]["date"])
    except Exception as e:
        raise ValueError(
            f"Last date is not extracted from table {table_name}: {str(e)}"
        )


# This code is used to insert data into airflow postgres db it not good practice
# to use to_sql in airflow database so we are using creating table and inserting
def load_to_db(df: pd.DataFrame, insert_query: str, table_name: str):
    """Load a DataFrame into PostgreSQL table"""
    try:
        hook = PostgresHook(postgres_conn_id="my_postgres_conn_id")
        conn = hook.get_conn()
        cursor = conn.cursor()
        data = list(
            df.drop(columns=["id"], errors="ignore").itertuples
            (index=False, name=None)
        )
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Inserted {cursor.rowcount} rows into {table_name}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise AirflowFailException(f"Failed to insert into {table_name}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_api_table(create_query: str):
    """Create a table in PostgreSQL."""

    try:
        with get_db_connection(DB_API_CONFIG) as conn:
            cursor = conn.cursor()
            cursor.execute(create_query)
            conn.commit()
            print(f"Table created or verified successfully")
    except PsycopgError as e:
        print(f"Failed to create table: {str(e)}")
        raise Exception(f"Failed to create table: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Database connection closed")


def load_api_db(df: pd.DataFrame, insert_query: str, table_name: str):
    """Load a DataFrame into a PostgreSQL table without Airflow dependency."""
    conn = None
    cursor = None
    try:
        with get_db_connection(DB_API_CONFIG) as conn:

            cursor = conn.cursor()

        # Convert DataFrame to list of tuples, excluding 'id' column if present
            data = list(
                df.drop(columns=["id"], errors="ignore").itertuples(
                    index=False, name=None
                )
            )

            # Execute the insert query
            cursor.executemany(insert_query, data)
            conn.commit()
            print(f"Inserted {cursor.rowcount} rows into {table_name}")

    except PsycopgError as e:
        if conn:
            conn.rollback()
        print(f"Failed to insert into {table_name}: {str(e)}")
        raise Exception(f"Failed to insert into {table_name}: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print(f"Database connection closed for {table_name}")
