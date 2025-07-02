"""Preprocesses data for ML model"""

import pandas as pd
import numpy as np
from utils.logger import get_logger
from config.config import DB_CONFIG
from utils.helper import (
    get_db_connection,
    load_to_db,
    truncate_table,
    create_table,
    is_new_data,
)
from scipy.stats.mstats import winsorize

logger = get_logger("model")


def clean_data(df: pd.DataFrame):
    """Preprocess data by scaling and handling outliers,
      loading from and saving to database"""

    # checking the missing and treating them
    try:
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())

            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].fillna(method="ffill")

            elif pd.api.types.is_categorical_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mode()[0])

        logger.info("Imputate missing values successfully")

        # Dealing with the outlier with IQR method
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]) and col not in ["id", "version"]:
                df[col] = pd.Series(np.asarray(winsorize(df[col], limits=[0.05, 0.05])))

        logger.info("Capping the outlier successfully")

    except Exception as e:
        logger.error(f"Preprocessing failed: {str(e)}")
        raise

    return df


def preprocess_data(coin: str):
    # connecting to Postgres database
    table_name = f"preprocessed_{coin}"
    raw_table = f"prices_{coin}"

    create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            price FLOAT NOT NULL,
            coin VARCHAR(50) NOT NULL,
            version INT DEFAULT 1
        )
        """
    create_table(create_query)

    try:
        last_date = is_new_data(coin, table_name)
    except Exception as e:
        logger.warning(
            f"Could not fetch latest date from {table_name}, preceeding with full dat reason for it {str(e)}"
        )
        last_date = None
    try:
        with get_db_connection(DB_CONFIG) as conn:
            if last_date:
                query = f"SELECT timestamp, price, coin FROM  {raw_table} WHERE timestamp > %s"
                df = pd.read_sql(query, conn, params=[last_date])
                if df.empty:
                    logger.warning(
                        f"No new data after {last_date}. Loading full table as fallback."
                    )
                    return None
            else:
                df = pd.read_sql(
                    f"SELECT timestamp, price, coin FROM {raw_table}", conn
                )

            logger.info(f"Loaded data sucessfully from {raw_table}")
    except Exception as e:
        logger.error(f"Load data from {coin}: is failed{str(e)}")
        raise

    if df.empty:
        logger.warning(f"No data for this {coin}")
        return None
    df.rename(columns={"timestamp": "date"}, inplace=True)
    df["version"] = 1
    cleaned_df = clean_data(df)

    insert_query = f"""
        INSERT INTO {table_name} (date, price, coin, version)
        VALUES (%s, %s, %s, %s)
    """
    # Load conditionally
    if last_date:
        load_to_db(cleaned_df, insert_query, table_name)
        logger.info(f"Appended new historical data for {coin} to {table_name}")
    else:
        truncate_table(table_name)
        load_to_db(cleaned_df, insert_query, table_name)
        logger.info(f"Replaced {table_name} with initial cleaned data for {coin} ")
