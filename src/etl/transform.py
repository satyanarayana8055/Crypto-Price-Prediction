"""Transforms raw cryptocurrency data"""
import os
import sys
import pandas as pd
from utils.helper import ensure_directory, validate_dataframe
from utils.logger import get_logger
from config.config import DATA_PATHS

logger = get_logger('etl')

def transform_coin_data(raw_file: str) -> str:
    """Transform raw data for a single coin"""
    try:
        df = pd.read_csv(raw_file)
        coin = df['coin'].iloc[0]
        validate_dataframe(df, expected_columns=['date', 'price', 'coin'])
        df['daily_return'] = df['price'].pct_change()
        df['ma_7'] = df['price'].rolling(window=7).mean()
        df['ma_14'] = df['price'].rolling(window=14).mean()
        df = df.dropna()
        validate_dataframe(df, expected_columns=['date', 'price', 'coin', 'daily_return', 'ma_7', 'ma_14'])
        
        output_file = os.path.join(DATA_PATHS['processed'],f'{coin}_transformed.csv')
        ensure_directory(DATA_PATHS['processed'])
        df.to_csv(output_file, index=False)
        logger.info(f"Transformed {coin} data to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Error transforming {raw_file}: {str(e)}")
        raise

def transform_all_coins(raw_files: list) -> list:
    """Transform all raw data files"""
    output_paths = []
    for raw_file in raw_files: 
        try:
            output_path = transform_coin_data(raw_file)
            output_paths.append(output_path)
        except Exception as e:
            logger.error(f"Skipping {raw_file} due to error: {str(e)}")
            continue
        return output_paths
if __name__ == "__main__":
    transform_coin_data(sys.argv[1])


"""
This script is designed to transform cryptocurrency CSV data files.

It supports both:
- Single CSV file processing
- Multiple CSV files processing

Usage from the terminal:
    python script.py <file1.csv> [<file2.csv> <file3.csv> ...]

How it works:
    - The script reads all file paths passed as command-line arguments (via sys.argv[1:])
    - If one file is provided, it calls `transform_coin_data()` directly.
    - If multiple files are provided, it uses `transform_all_coins()` to process them in a loop.

Example:
    python script.py data/raw/bitcoin.csv data/raw/ethereum.csv
"""
