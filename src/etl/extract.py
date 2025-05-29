"""Extracts daily cryptocurrency price data from CoinGecko"""
import os 
import time
import pandas as pd
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI
from requests.exceptions import RequestException
from utils.logger import get_logger
from utils.helper import ensure_directory, validate_dataframe
from config.config import COINGECKO_CONFIG, DATA_PATHS

logger = get_logger('etl')

def extract_coin_data(coin: str, start_date: datetime, end_date: datetime, retries: int = 3) -> str :
    """Incrementally extract and append daily price data for a coin"""

    client = CoinGeckoAPI()
    from_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
    to_ts = int(datetime.combine(end_date, datetime.min.time()).timestamp())
    attempt = 0 
 
    while attempt < retries:
        try:
            data = client.get_coin_market_chart_range_by_id(id=coin, vs_currency='usd', from_timestamp=from_ts, to_timestamp=to_ts)
            prices =data.get('prices', [])
            if not prices:
                logger.warning(f"No data for {coin} from {start_date.date()} to {(start_date + timedelta(days=30)).date()}")
                return None

            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
            df = df.groupby(df['timestamp'].dt.date).agg({'price': 'mean'}).reset_index()
            df.rename(columns={'timestamp': 'date'},inplace=True)
            df['date'] = pd.to_datetime(df['date'])
            df['coin'] = coin
            
            # Load existing csv if available 
            output_file = os.path.join('/app/data/raw/', f'{coin}_data.csv')
            ensure_directory('app/data/raw')
            
            if os.path.exists(output_file):
                old_df = pd.read_csv(output_file, parse_dates=['date'])
                combined_df = pd.concat([old_df,df])
                combined_df = combined_df.drop_duplicates(subset='date', keep='first')
            else:
                combined_df = df
            
            combined_df = combined_df.sort_values('date').reset_index(drop=True)
            
            validate_dataframe(combined_df, expected_columns=['date', 'price', 'coin'])
            combined_df.to_csv(output_file, index=False)
            logger.info(f"Updated data for {coin} saved to {output_file}")
            return output_file

        except RequestException as e:
            attempt += 1
            logger.warning(f"Attempt {attempt} failed for {coin}: {str(e)}")
            time.sleep(2)
            if attempt == retries:
                logger.error(f"Failed to extract {coin} data after {retries} attempts")
                raise
            
def extract_all_coins(start_date: datetime, end_date: datetime) -> list:
    """Extract data for all configured coins"""
    output_paths = []
    coins = COINGECKO_CONFIG['coins']
    for coin in coins:
        try:
            output_path = extract_coin_data(coin, start_date, end_date)
            output_paths.append(output_path)
        except Exception as e:
            logger.error(f"Skipping {coin} due to error: {str(e)}")
            continue
    return output_paths

if __name__ == "__main__":
    end_date = datetime.today()
    start_date = end_date - timedelta(days=364)
    extract_all_coins(start_date=start_date, end_date=end_date)
    