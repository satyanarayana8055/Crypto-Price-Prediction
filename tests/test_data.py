"""Teest for data extraction and validation"""
import os
import pytest
import pandas as pd
from utils.helper import validate_dataframe
from config.config import DATA_PATHS, COINS
expected_columns = [
    'coin', 'timestamp', 'price', 'market_cap', 'volume',
    'price_change_24h', 'price_change_percentage_24h'
]
@pytest.mark.parametrize("coin", COINS)
def test_extracted_df(coin):
    output_path = os.path.join(DATA_PATHS['raw'],f'{coin}_data.csv')
    
    # Assert file exists
    assert os.path.exists(output_path), f"CSV not found at {output_path}"
   
    # Load and validating data
    df = pd.read_csv(output_path, parse_dates=['timestamp'])
    validate_dataframe(df, expected_columns)

    # Column-level tests
    assert df['price'].notnull().all(), "Null values in 'price'"

    for col in ['market_cap', 'volume']:
        assert (df[col] >= 0).all(), f"{col} contains negative values"
  
    # Consistency checks
    assert df['coin'].nunique() == 1
    assert df['coin'].iloc[0].lower() == coin

    # Timestamp checks
    assert df['timestamp'].is_monotonic_increasing, "Timestamps not sorted"
    assert not df.duplicated(subset=['timestamp', 'coin']).any(), "Duplicate (coin, timestamp) rows found"
