"""Extracts daily cryptocurrency price data from CoinGecko"""

import os
import time
import requests
import pandas as pd
from datetime import datetime
from requests.exceptions import RequestException
from utils.logger import get_logger
from utils.helper import ensure_directory, validate_dataframe
from config.config import DATA_PATHS, Web

logger = get_logger("etl")


def extract_coin_data(
    coin: str, start_date: datetime, end_date: datetime, retries: int = 3
) -> str:
    """Extract daily data using CoinGecko API and save as CSV"""

    from_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
    to_ts = int(datetime.combine(end_date, datetime.min.time()).timestamp())
    attempt = 0
    base_url = Web.COINGECKO_API_URL
    params = {"vs_currency": "usd", "from": from_ts, "to": to_ts}
    url = f"{base_url}/coins/{coin}/market_chart/range"
    while attempt < retries:
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            prices = data.get("prices", [])
            market_caps = data.get("market_caps", [])
            volumes = data.get("total_volumes", [])

            if not prices:
                logger.warning(
                    f"""No data for {coin} from {start_date.date()} 
                    to {end_date.date()}"""
                )
                return None

            # Convert to DataFrame
            df_prices = pd.DataFrame(prices, columns=["timestamp", "price"])
            df_market_cap = pd.DataFrame(
                market_caps, columns=["timestamp", "market_cap"]
            )
            df_volumes = pd.DataFrame(volumes, columns=["timestamp", "volume"])

            # Convert ms timestamp to datatime
            for df in [df_prices, df_market_cap, df_volumes]:
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            # merge all into one DataFrame
            df = df_prices.merge(df_market_cap, on="timestamp", how="left")
            df = df.merge(df_volumes, on="timestamp", how="left")

            # Add coin
            df["coin"] = coin

            # Sort and compute 24h price change
            df.sort_values("timestamp", inplace=True)
            df["price_change_24h"] = df["price"].diff()
            df["price_change_percentage_24h"] = (
                df["price_change_24h"] / df["price"].shift(1) * 100
            )

            # Reorder and rename columns to match SQL schema

            df = df[
                [
                    "coin",
                    "timestamp",
                    "price",
                    "market_cap",
                    "volume",
                    "price_change_24h",
                    "price_change_percentage_24h",
                ]
            ]

            # Load existing csv if available
            output_file = os.path.join(DATA_PATHS["raw"], f"{coin}_data.csv")

            try:
                ensure_directory(DATA_PATHS["raw"])
            except Exception as e:
                logger.error(
                    f"Failed to create directory {DATA_PATHS['raw']}: {str(e)}"
                )
                raise

            # Append to existing CSV if it exists
            if os.path.exists(output_file):
                old_df = pd.read_csv(output_file, parse_dates=["timestamp"])
                df = pd.concat([old_df, df])
                df = df.drop_duplicates(subset=["timestamp", "coin"],
                                         keep="first")

            df.sort_values("timestamp", inplace=True)
            df.reset_index(drop=True, inplace=True)

            validate_dataframe(
                df,
                expected_columns=[
                    "coin",
                    "timestamp",
                    "price",
                    "market_cap",
                    "volume",
                    "price_change_24h",
                    "price_change_percentage_24h",
                ],
            )

            # Save CSV and verify
            df.to_csv(output_file, index=False)
            if os.path.exists(output_file):
                logger.info
                (f"Successfully saved data for {coin} to {output_file}")
                return output_file
            else:
                logger.error(
                    f"""Failed to save data for {coin}
                      to {output_file}: File does not exist"""
                )
                raise OSError(f"CSV file {output_file} was not created")

        except RequestException as e:
            attempt += 1
            logger.warning(f"Attempt {attempt} failed for {coin}: {str(e)}")
            time.sleep(2)
            if attempt == retries:
                logger.error
                (f"Failed to extract {coin} data after {retries} attempts")
                raise
