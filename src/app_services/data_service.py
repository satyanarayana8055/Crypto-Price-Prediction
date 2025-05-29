import pandas as pd 
import glob # it is used to find the specific patter with file name has specific pattern
import os
from utils.logger import get_logger
from config.config import DATA_PATHS

logger = get_logger('data_service')

def get_latest_data(coin: str) -> dict:
    """Fetch latest data for a coin"""
    try:
        latest_file = sorted(glob.glob(os.path.join(DATA_PATHS['processed'], f'{coin}_transformed.csv')))[-1]
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]
        data = {
            'date': latest['date'],
            'price': latest['price'],
            'daily_return': latest['daily_return']
        }
        logger.info(f"Fetched latest data for {coin}")
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {coin}: {str(e)}")
        raise
