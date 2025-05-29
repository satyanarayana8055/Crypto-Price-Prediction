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
                   daily_return FLOAT,
                   ma_7 FLOAT,
                   ma_14 FLOAT,
                   coin VARCHAR(50) NOT NULL,
                   version INT DEFAULT 1
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
                records = [
                    (
                        row['date'],
                        row['price'],
                        row['daily_return'],
                        row['ma_7'],
                        row['ma_14'],
                        row['coin']
                    )
                    for _, row in df.iterrows()
                ]
                query = f""" 
                        INSERT INTO {table_name} (date, price, daily_return, ma_7, ma_14, coin) VALUES (%s, %s, %s, %s, %s, %s)
                        """
                execute_batch(cursor, query, records, page_size=1000)
                conn.commit()
                logger.info(f"Loaded {len(df)} records for {coin} to {table_name}")
    except psycopg2.Error as e:
        logger.error(f"Database error loading {transformed_file}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error loading {transformed_file}: {str(e)}")
        raise

def load_all_coins(transformed_files: list):
    """Load all transformed files"""
    for file in transformed_files:
        try: 
            load_to_db(file)
        except Exception as e:
            logger.error(f"Skipping {file} due to error: {str(e)}")
            continue

if __name__ == "__main__":
    load_to_db(sys.argv[1])