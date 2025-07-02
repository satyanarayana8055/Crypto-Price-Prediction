"""Transforms raw cryptocurrency data"""

import os
import pandas as pd
from utils.helper import ensure_directory, validate_dataframe
from utils.logger import get_logger
from config.config import DATA_PATHS

logger = get_logger("etl")


def transform_coin_data(raw_file: str) -> str:
    """Transform raw data for a single coin"""
    try:
        df = pd.read_csv(raw_file)
        coin = df["coin"].iloc[0]

        expected_cols = [
            "coin",
            "timestamp",
            "price",
            "market_cap",
            "volume",
            "price_change_24h",
            "price_change_percentage_24h",
        ]
        validate_dataframe(df, expected_columns=expected_cols)

        # Data cleaning steps
        df = df.dropna(
            subset=["price", "timestamp"]
        )  # Remove rows with missing critical data
        df = df[df["price"] > 0]
        df = df[df["volume"] >= 0]

        # Add minimal transformations if needed (e.g., rounging for consistency)
        df["price"] = df["price"].astype(float).round(2)
        df["volume"] = df["volume"].astype(float).round(2)
        df["market_cap"] = df["market_cap"].astype(float).round(2)
        df["price_change_24h"] = df["price_change_24h"].astype(float).round(2)
        df["price_change_percentage_24h"] = (
            df["price_change_percentage_24h"].astype(float).round(2)
        )

        # Ensure chronogical order
        df = df.sort_values("timestamp")

        output_file = os.path.join(DATA_PATHS["transfrom"],
                                   f"{coin}_transformed.csv")
        ensure_directory(DATA_PATHS["transfrom"])
        df.to_csv(output_file, index=False)
        logger.info(f"Transformed {coin} data to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Error transforming {raw_file}: {str(e)}")
        raise


"""
This script is designed to transform cryptocurrency CSV data files.

It supports both:
- Single CSV file processing
- Multiple CSV files processing

Usage from the terminal:
    python script.py <file1.csv> [<file2.csv> <file3.csv> ...]

How it works:
    - The script reads all file paths passed as command-line
    arguments (via sys.argv[1:])
    - If one file is provided, it calls `transform_coin_data()` directly.
    - If multiple files are provided, it uses `transform_all_coins()`
    to process them in a loop.

Example:
    python script.py data/raw/bitcoin.csv data/raw/ethereum.csv
"""
