import os
import pandas as pd
from datetime import datetime, timedelta
import requests
from config.config import Web, API_PATHS
from utils.helper import load_api_db, create_api_table
from utils.logger import get_logger


logger = get_logger('etl')


def fetch_coin_data(coin_ids, days):
    base_url = Web.COINGECKO_API_URL
    vs_currency = "usd"
    all_data = []

    for coin in coin_ids:
        try:
            url = f"{base_url}/coins/{coin}/market_chart"
            params = {
                "vs_currency": vs_currency,
                "days": days,
                "interval": "daily"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            prices = data.get("prices", [])
            volumes = data.get("total_volumes", [])
            market_caps = data.get("market_caps", [])

            for i in range(len(prices)):
                ts = datetime.fromtimestamp(prices[i][0] / 1000)

                price = prices[i][1]
                volume = volumes[i][1] if i < len(volumes) else None
                market_cap = market_caps[i][1] if i < len(market_caps) else None

                # Calculate 24h change and percentage
                if i > 0:
                    prev_price = prices[i - 1][1]
                    price_change = price - prev_price
                    pct_change = (price_change / prev_price) * 100 if prev_price != 0 else 0
                else:
                    price_change = None
                    pct_change = None

                all_data.append({
                    "coin_id": coin,
                    "timestamp": ts.isoformat(),
                    "price": price,
                    "market_cap": market_cap,
                    "volume": volume,
                    "price_change_24h": price_change,
                    "price_change_percentage_24h": pct_change
                })

        except Exception as e:
            logger.error(f"Failed to fetch data for {coin}: {e}")

        # Clean and insert after fetching all coins
        clean_df = clean_data(pd.DataFrame(all_data))

        table_name = "crypto_prices"
        create_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                coin_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                price REAL NOT NULL,
                market_cap REAL,
                volume REAL,
                price_change_24h REAL,
                price_change_percentage_24h REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (coin_id, timestamp) 
            )

        """
        create_api_table(create_query)
        insert_query = f"""INSERT INTO crypto_prices 
                    (coin_id, timestamp, price, market_cap, volume, price_change_24h, price_change_percentage_24h)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (coin_id, timestamp) DO NOTHING;
                    """
        df = load_api_db(clean_df, insert_query, table_name)
    return df

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
     # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sort by timestamp (just in case)
    df.sort_values(by='timestamp', inplace=True)

    # Forward fill, then backfill remaining if any
    df.ffill(inplace=True)
    df.bfill(inplace=True)

    # Drop any rows that are still completely empty (edge case)
    df.dropna(how='all', inplace=True)

    # Reset index (good for clean display)
    df.reset_index(drop=True, inplace=True)

    return df

# === RUN & SAVE TO CSV ===
if __name__ == "__main__":
    coin_ids = ['bitcoin', 'ethereum', 'cardano', 'solana']
    days = 365

    fetch_coin_data(coin_ids, days)
