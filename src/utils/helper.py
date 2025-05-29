"""Reusable utility functions for CryptoPredictor"""
import os
import pandas as pd
import psycopg2
from pathlib import Path
from contextlib import contextmanager # Decorator to write custom context managers using generator functions instead of classes
from config.path_config import DATA_PATHS

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