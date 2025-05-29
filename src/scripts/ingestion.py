"""Ingests transformed data from DB for ML pipeline"""
import os
import sys
import pandas as pd
from utils.logger import get_logger
from config.config import DATA_PATHS


logger = get_logger('model')

def ingest_data(coin: str = None) -> pd.DataFrame:
    """Ingest data for a specific coin or all coins"""

    try:
        pattern = f'{coin}_transformed.csv' if coin else '*_transformed.csv'
        files = [os.path.join(DATA_PATHS['processed'],f) 
                 for f in os.listdir(DATA_PATHS['processed']) 
                 if f.endswith ('.csv') and pattern in f]
        if not files: 
            raise FileNotFoundError(f"No data files found for {coin or 'all coins'}")
        df_list = [pd.read_csv (f) for f in files]
        combined_df = pd.concat(df_list, ignore_index=True)
        logger.info(f"Ingested {len(combined_df)} total records for {coin or 'all coins'}")
        return combined_df
    except Exception as e:
        logger.error(f"Error ingesting data: {str(e)}")
        raise

if __name__ == "__main__":
# for this i need to mention the coin name like this python src/scripts/ingestion.py bitcoin
    coin = sys.argv[1] if len(sys.argv) > 1 else None 
    ingest_data(coin)