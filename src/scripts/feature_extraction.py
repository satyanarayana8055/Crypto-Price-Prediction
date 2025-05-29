import os
import sys
import pandas as pd 
from utils.logger import get_logger
from scripts.ingestion import ingest_data
from scripts.preprocessing import preprocess_data

logger = get_logger('model')

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract features like moving averages"""
    try:
        df['lag_price_1'] = df['price'].shift(1)
        df['lag_price_2'] = df['price'].shift(2)
        df['lag_return_1'] = df['daily_return'].shift(1)
        
        # Safe rolling calculations (using closed = 'left')
        df['ma_7'] = df['price'].shift(1).rolling(window=7, min_periods=1, closed='left').mean()
        df['ma_14'] = df['price'].shift(1).rolling(window=14, min_periods=1, closed='left').mean()

        # Return to MA ratios
        df['return_ma_ratio_7'] = df['daily_return'] / (df['ma_7'] + 1e-6 )
        df['return_ma_ratio_14'] = df['daily_return'] / (df['ma_14'] + 1e-6)

        # Rolling standard deviation as a proxy for volatility
        df['price_volatility_7'] = df['price'].rolling(window=7).std()

        # Drop rows with NaN due to rolling and shifting
        df = df.dropna() 
        logger.info("Feature extraction completed successfully")
        return df       
    except Exception as e:
        logger.error(f"Error extracting features: {str(e)}")
        raise

if __name__ == "__main__":
        try: 
           coin = sys.argv[1]
           output_path = sys.argv[2] 
           df = ingest_data(coin)
           df, _ = preprocess_data(df)
           df = extract_features(df)
           os.makedirs(os.path.dirname(output_path), exist_ok=True)
           df.to_csv(output_path, index=False)
           logger.info(f"Feature enriched data saved to: {output_path}")

        except Exception as e:
           logger.error(f"Error in main: {str(e)}")
           raise
      
                       