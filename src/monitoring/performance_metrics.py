"""Tracks model performance metrics"""
import pandas as pd
import os
import sys
from utils.logger import get_logger
from config.config import DATA_PATHS

logger = get_logger('monitor')

def log_performance(metrics: dict, coin: str):
    """Log performance metrics for a coin"""
    try:
        metrics_df = pd.DataFrame({
            'date': [pd.Timestamp.now()],
            'coin': [coin],
            'mse': [metrics['mse']],
            'r2': [metrics['r2']],
            'mae': [metrics['mae']]
        })
        metrics_path = os.path.join(DATA_PATHS['processed'], f'{coin}_metrics.csv')
        if os.path.exists(metrics_path):
            existing = pd.read_csv(metrics_path)
            metrics_df = pd.concat([existing, metrics_df], ignore_index=True)
        metrics_df.to_csv(metrics_path, index=False)
        logger.info(f"Logger metrics for {coin} to {metrics_path}")
    except Exception as e:
        logger.error(f"Error logged metrics for {coin}: {str(e)}")
        raise

if __name__ == "__main__":
    metrics = {'mse': float(sys.argv[1]), 'r2': float(sys.argv[2]), 'mae': float(sys.argv[3])}
    coin = sys.argv[4]
    log_performance(metrics, coin)