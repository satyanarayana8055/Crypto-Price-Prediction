"""Reusable utility functions for CryptoPredictor"""
import os
import pandas as pd
import psycopg2
import re
from pathlib import Path
from contextlib import contextmanager # Decorator to write custom context managers using generator functions instead of classes
from config.path_config import DATA_PATHS, DB_CONFIG
from datetime import datetime, timedelta
from airflow.hooks.postgres_hook import PostgresHook
from airflow.exceptions import AirflowFailException
from typing import Optional

def ensure_directory(path: str):
    """Create directory if it doesn't exist."""
    # It is the base folder to get access from outside the src folder 
    
    dir_path = DATA_PATHS.get(path, Path(path))
    if not isinstance (dir_path, Path):
        dir_path = Path(dir_path)
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_dataframe(df: pd.DataFrame, expected_columns: list):
    """Validate DataFrame structure it ensure the data is correct extracted base on our requirements"""
    if df.empty:
        raise ValueError("DataFrame is empty")
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns :
        raise ValueError(f"Missing columns: {missing_columns}")
    
@contextmanager
def get_db_connection(config: dict):
    """Context manager for PostgreSQL connections.
    Establishes a DB connection and yields it.
    The connection is automatically closed when the block exits."""
    conn = None 
    try:
        conn = psycopg2.connect(**config) 
        yield conn # It is used to used to return object temporarily to caller and pause untill caller is done
    finally:
        if conn:
            conn.close()

# Trucated table is more faster than deleting the table because it remove complete data srcipt one time from data table without removing the table structure
def truncate_table(table_name: str):
    """Deletes all data from a table"""
    try:
        hook = PostgresHook(postgres_conn_id='my_postgres_conn_id')
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
    """Creates the table if not exists and ensures the unique constraint is applied"""
    try:
        hook = PostgresHook(postgres_conn_id='my_postgres_conn_id')
        conn = hook.get_conn()
        cursor = conn.cursor()
        
        cursor.execute(create_query)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise AirflowFailException(f"Failed to create table or add constraint: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def is_new_data(coin: str, table_name: str) -> Optional[datetime]:
    try:
        with get_db_connection(DB_CONFIG) as conn:
            df = pd.read_sql(f"SELECT * FROM {table_name} ORDER BY date DESC LIMIT 1", conn)
            
            if df.empty:
                return None

            return pd.to_datetime(df.iloc[0]['date'])
    except Exception as e:
        raise ValueError(f"Last date is not extracted from table {table_name}: {str(e)}")

# This code is used to insert data into airflow postgres db it not good practice to use to_sql in airflow database so we are using creating table and inserting
def load_to_db(df: pd.DataFrame, insert_query: str, table_name: str):
    """Load a DataFrame into PostgreSQL table"""
    try:
        hook = PostgresHook(postgres_conn_id='my_postgres_conn_id')
        conn = hook.get_conn()
        cursor = conn.cursor()
        data = list(df.drop(columns=['id']).itertuples(index=False, name=None))
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Inserted {cursor.rowcount} rows into {table_name}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise AirflowFailException (f"Failed to insert into {table_name}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# def gen_next_version_path(base_dir: str, coin: str) -> str:
#     Path(base_dir).mkdir(parents=True, exist_ok=True)
#     existing_files = os.listdir(base_dir)
#     version_pattern = re.compile(rf"{coin}_model_v(\d+)\.pkl")
#     versions = []

#     for f in existing_files:
#         match = version_pattern.match(f)
#         if match:
#             versions.append(int(match.group(1)))
    
#     next_version = max(versions, default=0) + 1
#     file_name = f"{coin}_model_v{next_version}.pkl"

#     return os.path.join(base_dir, file_name)

# def is_historical_data(coin: str, table_name: str) -> bool:

#     """Check if historical data is exists for the coin"""

#     try: 
#         with get_db_connection(DB_CONFIG) as conn:
#             df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
#             if df.empty:
#                 return False
#             df['date'] = pd.to_datetime(df['date'])
#             recent_df = df.sort_values(by='date').tail(545)
#             earlier_date = recent_df['date'].min()

#             # if earlier_date - recent_df[0] == timedelta(days=180):
#             today = datetime.today()
#             half_annual = today - timedelta(days=180)
#             one_year = timedelta(days=365)

#             if (half_annual - earlier_date) >= one_year:
#                 return True
#             else:
#                 return False
                  
#     except Exception as e:
#         raise ValueError(f"Error checking historical data for {coin}: {str(e)}")

# """if you want to connect the trucate and load_db in modular way this code can be usefull"""
# from contextlib import contextmanager
# from airflow.hooks.postgres_hook import PostgresHook
# import logging

# logger = logging.getLogger(__name__)

# @contextmanager
# def get_db_cursor(postgres_conn_id='my_postgres_conn_id'):
#     """Context manager to get a Postgres cursor and connection with automatic cleanup."""
#     hook = PostgresHook(postgres_conn_id=postgres_conn_id)
#     conn = None
#     cursor = None
#     try:
#         conn = hook.get_conn()
#         cursor = conn.cursor()
#         yield cursor, conn
#         conn.commit()
#     except Exception as e:
#         if conn:
#             conn.rollback()
#         logger.error(f"Database error: {str(e)}")
#         raise
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()

# def truncate_table(table_name: str):
#     """Truncate a table using the context manager."""
#     with get_db_cursor() as (cursor, conn):
#         cursor.execute(f"TRUNCATE TABLE {table_name}")
#         logger.info(f"Truncated existing data from {table_name}")