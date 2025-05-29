"""Teest for data extraction and validation"""
import pytest
import pandas as pd
from etl.extract import extract_coin_data
from utils.helper import validate_dataframe
def test_data_extraction():
    """Test data extraction for a coin"""
    output_path = extract_coin_data('bitcoin')
    df = pd.read_csv(output_path)
    assert not df.empty, "Extracted data is empty"
    assert 'date' in df.columns, "Timestamp column missing"
    assert 'price' in df.columns, "Price columns missing"
    assert 'coin' in df.columns, "Coin columns missing"

def test_empty_data():
    """Test handling of empty data"""
    with pytest.rasie(ValueError):
        df = pd.DataFrmae()
        validate_dataframe(df, ['timestamp', 'price'])

if __name__ == "__main__":
    pytest.main()