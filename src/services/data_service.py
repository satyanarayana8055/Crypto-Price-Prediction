from utils.logger import get_logger
from config.config import DB_CONFIG, Web
import requests
from datetime import datetime, timedelta
import time
from utils.helper import get_db_connection


logger = get_logger("service")


class DataService:
    """Service for fetching cryptocurrency data using CoinGecko API"""

    def __init__(self):
        self.base_url = Web.COINGECKO_API_URL
        self.cache = {}
        self.cache_duration = Web.CACHE_DURATION

    def get_live_data(self, coin):
        """Get live data from CoinGecko API or fallback to database"""
        try:
            # Check cache first
            cache_key = f"live_data_{coin}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]["data"]
            # Try to get live data from CoinGecko
            url = f"{self.base_url}/simple/price"
            params = {
                "ids": coin,
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_last_updated_at": "true",
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if coin in data:
                coin_data = data[coin]

                self.cache[cache_key] = {"data": coin_data, 
                                         "timestamp": time.time()}
                return {
                    "coin": coin,
                    "price": coin_data["usd"],
                    "market_cap": coin_data.get("usd_market_cap"),
                    "volume": coin_data.get("usd_24h_vol"),
                    "price_change_24h": coin_data.get("usd_24h_change"),
                    "last_updated": datetime.fromtimestamp(
                        coin_data.get("last_updated_at", 0)
                    ),
                    "source": "live",
                }
            else:
                raise Exception(f"No data found for {coin}")
        except Exception as e:
            print(f"Error fetching live data: {e}")
            return self.get_latest_from_db(coin)

    def get_historical_data(self, coin, days=30):
        """get historical price data"""
        try:
            cache_key = f"historical_{coin}_{days}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]["data"]

            url = f"{self.base_url}/coins/{coin}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "daily" if days > 30 else "hourly",
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            # Formate data for charts
            prices = []
            for timestamp, price in data["prices"]:
                prices.append(
                    {
                        "timestamp": datetime.fromtimestamp(timestamp / 1000),
                        "price": price,
                    }
                )
            self.cache[cache_key] = {"data": prices, "timestamp": time.time()}
            return {"coin": coin, "prices": prices, "source": "live"}
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return self.get_historical_from_db(coin, days)

    def get_latest_from_db(self, coin):
        """Get latest data from database"""
        try:
            with get_db_connection(DB_CONFIG) as conn:
                cursor = conn.cursor()
                table_name = f"prices_{coin}"
                cursor.execute(
                    f"""
                    SELECT * FROM {table_name}
                            WHERE coin = %s
                            ORDER BY timestamp DESC
                            LIMIT 1
                            """,
                    (coin,),
                )
                row = cursor.fetchone()

                if row:
                    return {
                        "coin": coin,
                        "price": row[3],
                        "market_cap": row[4],
                        "volume": row[5],
                        "price_change_24h": row[6],
                        "last_updated": (
                            row[2]
                            if isinstance(row[2], datetime)
                            else datetime.fromisoformat(row[2])
                        ),
                        "source": "database",
                    }
                else:
                    return {"error": "No data available"}

        except Exception as e:
            print(f"Database error: {e}")
            return {"error": "Database error"}

    def get_historical_from_db(self, coin, days):
        """Get historical data from database"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            with get_db_connection(DB_CONFIG) as conn:
                table_name = f"prices_{coin}"
                cursor = conn.cursor()
                cursor.execute(
                    f"""
                    SELECT timestamp, price FROM {table_name}
                            WHERE coin = %s AND timestamp >= %s
                            ORDER BY timestamp ASC 
                            """,
                    (coin, start_date),
                )
                rows = cursor.fetchall()

                prices = []
                for row in rows:
                    prices.append({"timestamp": row[0], "price": row[1]})

                return {"coin": coin, "prices": prices, "source": "database"}

        except Exception as e:
            print(f"Database error: {e}")
            return {"error": "Database error"}

    def get_supported_coins(self):
        """Get list of supported coins"""
        return [
            {"id": "bitcoin", "name": "Bitcoin", "symbol": "BTC"},
            {"id": "ethereum", "name": "Ethereum", "symbol": "ETH"},
            {"id": "cardano", "name": "Cardano", "symbol": "ADA"},
            {"id": "solana", "name": "Solana", "symbol": "SOL"},
        ]

    def _is_cache_valid(self, key):
        """Check if cached data is still  valid"""
        if key not in self.cache:
            return False
        cache_time = self.cache[key]["timestamp"]
        return (time.time() - cache_time) < self.cache_duration
