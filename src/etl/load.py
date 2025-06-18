import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch # we can insert multiple rows at once
from utils.helper import get_db_connection 
from utils.logger import get_logger
from config.config import DB_CONFIG, TABLE_NAME

logger = get_logger('etl')

def create_table(cursor, coin: str):
    """Create table for a coin"""
    table_name = TABLE_NAME[coin]
    cursor.execute(f"""
                   CREATE TABLE IF NOT EXISTS {table_name} (
                   id SERIAL PRIMARY KEY,
                   date TIMESTAMP NOT NULL,
                   price FLOAT NOT NULL,
                   coin VARCHAR(50) NOT NULL,
                   version INT DEFAULT 1, 
                   CONSTRAINT unique_date_coin UNIQUE (date, coin)
                   )
                   """)
    
def load_to_db(transformed_file: str):
    """Load transformed data into DB"""
    try:
        df = pd.read_csv(transformed_file)
        coin = df['coin'].iloc[0]
        table_name = TABLE_NAME[coin]
        with get_db_connection(DB_CONFIG) as conn:
            with conn.cursor() as cursor:            
                create_table(cursor, coin)
                # Check existing dates to avoid duplicates 
                cursor.execute(f"SELECT date FROM {table_name}")
                existing_dates = set(row[0] for row in cursor.fetchall())
                
                # Filter out existing dates
                df['date'] = pd.to_datetime(df['date'])
                new_data = df[~df['date'].isin(existing_dates)]

                if new_data.empty:
                    logger.info(f"No new data to load for {coin}")
                    return 
                
                records = [
                    (
                        row['date'],
                        row['price'],
                        row['coin']
                    )
                    for _, row in new_data.iterrows()
                ]
                query = f""" 
                        INSERT INTO {table_name} (date, price, coin) VALUES (%s, %s, %s)
                        ON CONFLICT ON CONSTRAINT unique_date_coin DO NOTHING
                        """
                execute_batch(cursor, query, records, page_size=1000)

                conn.commit()
                logger.info(f"Loaded {len(new_data)} new records for {coin} to {table_name}")
  
    except psycopg2.Error as e:
        logger.error(f"Database error loading {transformed_file}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error loading {transformed_file}: {str(e)}")
        raise
