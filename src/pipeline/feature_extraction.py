"""Extraction data for ML model"""

import pandas as pd
from utils.logger import get_logger
from config.config import DB_CONFIG
from utils.helper import (
    get_db_connection,
    load_to_db,
    truncate_table,
    create_table,
    is_new_data,
)

logger = get_logger("model")


def feature_engineering(df: pd.DataFrame):
    """Extracting features for building model needed features"""

    # checking the missing and treating them
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error(f"Expected pandas DataFrame, got {type(df)}")
            raise TypeError(f"Input must be a pandas DataFrame, got {type(df)}")
        for lag in [1, 2, 3, 7, 14]:
            df[f"lag_{lag}"] = df["price"].shift(lag)

        # Rolling mean and std
        df["rolling_mean_3"] = df["price"].rolling(window=3).mean()
        df["rolling_std_3"] = df["price"].rolling(window=3).std()

        df["rolling_mean_7"] = df["price"].rolling(window=7).mean()
        df["rolling_std_7"] = df["price"].rolling(window=7).std()

        df["rolling_max_7"] = df["price"].rolling(window=7).max()
        df["rolling_min_7"] = df["price"].rolling(window=7).min()

        # Price change in daily basics and weekly bases
        df["price_diff"] = df["price"].diff()
        df["pct_change_1"] = df["price"].pct_change()
        df["pct_change_7"] = df["price"].pct_change(periods=7)

        # capturing seasonality with datetime
        df["day_of_week"] = df["date"].dt.dayofweek
        df["day_of_month"] = df["date"].dt.day
        df["month"] = df["date"].dt.month
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

        # Trending and Volatility indicators
        df["exp_moving_avg_10"] = df["price"].ewm(span=10, adjust=False).mean()
        df["volatility_10"] = df["price"].rolling(10).std()

        # Target Feature
        df["target"] = df["price"].shift(-1)

    except Exception as e:
        logger.error(f"Preprocessing failed: {str(e)}")
        raise

    return df


def extract_features(coin: str):
    # connecting to Postgres database
    table_name = f"extract_features_{coin}"
    raw_table = f"preprocessed_{coin}"

    create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            price FLOAT NOT NULL,
            coin VARCHAR(50) NOT NULL,
            version INT DEFAULT 1,
            lag_1 FLOAT,
            lag_2 FLOAT,
            lag_3 FLOAT,
            lag_7 FLOAT,
            lag_14 FLOAT,
            rolling_mean_3 FLOAT,
            rolling_std_3 FLOAT,
            rolling_mean_7 FLOAT,
            rolling_std_7 FLOAT,
            rolling_max_7 FLOAT,
            rolling_min_7 FLOAT,
            price_diff FLOAT,
            pct_change_1 FLOAT,
            pct_change_7 FLOAT,
            day_of_week INT,
            day_of_month INT,
            month INT,
            is_weekend INT,
            exp_moving_avg_10 FLOAT,
            volatility_10 FLOAT,
            target FLOAT
        )
        """
    create_table(create_query)

    try:
        last_date = is_new_data(coin, table_name)
    except Exception as e:
        logger.warning(
            f"Could not fetch latest date from {table_name}, preceeding with full data reason for it {str(e)}"
        )
        last_date = None
    try:
        with get_db_connection(DB_CONFIG) as conn:
            if last_date:
                query = f"SELECT * FROM  {raw_table} WHERE date > %s"
                df = pd.read_sql(query, conn, params=[last_date])
                if df.empty:
                    logger.warning(
                        f"No new data after {last_date}. Loading full table as fallback."
                    )
                    return None
            else:
                df = pd.read_sql(f"SELECT * FROM {raw_table}", conn)
            logger.info(f"Loaded data sucessfully from {raw_table}")
    except Exception as e:
        logger.error(f"Load data from {coin}: is failed{str(e)}")
        raise

    if df.empty:
        logger.warning(f"No data for this {coin}")
        return None

    cleaned_df = feature_engineering(df)
    # features_path = os.path.join(DATA_PATHS['processed'],f"extract_features_{coin}.csv")
    # cleaned_df.to_csv(features_path, index=False)

    insert_query = f"""
        INSERT INTO {table_name} (date, price, coin, version,
                    lag_1, lag_2, lag_3, lag_7, lag_14, 
                    rolling_mean_3, rolling_std_3, rolling_mean_7, 
                    rolling_std_7, rolling_max_7, rolling_min_7,
                    price_diff, pct_change_1, pct_change_7,
                    day_of_week, day_of_month, month, is_weekend,
                    exp_moving_avg_10, volatility_10, target)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Load conditionally
    if last_date:
        load_to_db(cleaned_df, insert_query, table_name)
        logger.info(f"Appended new historical data for {coin} to {table_name}")
    else:
        truncate_table(table_name)
        load_to_db(cleaned_df, insert_query, table_name)
        logger.info(f"Replaced {table_name} with initial cleaned data for {coin} ")
