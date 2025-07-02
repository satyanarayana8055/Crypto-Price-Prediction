"""Loading CSV to database"""

import pandas as pd
from utils.helper import create_table, load_to_db
from utils.logger import get_logger

logger = get_logger("etl")


def load_to_database(transformed_file: str):
    """Load transformed data into DB"""
    try:
        df = pd.read_csv(transformed_file)
        coin = df["coin"].iloc[0]
        table_name = f"prices_{coin}"
        create_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                coin TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                price REAL NOT NULL,
                market_cap REAL,
                volume REAL,
                price_change_24h REAL,
                price_change_percentage_24h REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        create_table(create_query)
        insert_query = f"""INSERT INTO {table_name} 
                    (coin, timestamp, price, market_cap, volume, price_change_24h, price_change_percentage_24h)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """
        load_to_db(df, insert_query, table_name)
        logger.info(f"Loaded {len(df)} new records for {coin} to {table_name}")

    except Exception as e:
        logger.error(f"Error loading {transformed_file}: {str(e)}")
        raise
