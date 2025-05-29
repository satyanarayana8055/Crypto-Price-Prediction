"""Preprocesses data for ML model"""
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scripts.ingestion import ingest_data
from utils.logger import get_logger

logger = get_logger('model')

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess data by scaling and handling outliers"""
    try:
        df = df.fillna(method='ffill')
        df = df[df['price'].between(df['price'].quantile(0.01), df['price'].quantile(0.99))]
        scaler = StandardScaler()
        df[['price', 'daily_return', 'ma_7', 'ma_14']] =scaler.fit_transform(df[['price', 'daily_return', 'ma_7', 'ma_14']])
        logger.info("Preprocessed data")
        return df, scaler
    except Exception as e:
        logger.error(f"Error preprocessing data: {str(e)}")
        raise
if __name__ == "__main__":
    coin = sys.argv[1] if len(sys.argv) > 1 else None
    df = ingest_data(coin)
    df, scaler = preprocess_data(df)
    output_path = sys.argv[2]
    df.to_csv(output_path, index=False)