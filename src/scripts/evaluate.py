from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os
import joblib
import pandas as pd
from utils.logger import get_logger
from config.config import DB_CONFIG, DATA_PATHS
from scripts.model import prepare_data
from utils.helper import get_db_connection
logger = get_logger('model')

def split_data(coin: str):
    table_name = f'extract_features_{coin}'

    try: 
        with get_db_connection(DB_CONFIG) as conn:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)
            
            return prepare_data(df)
        
    except Exception as e:
        logger.error(f"failed to split the {str(e)}")
        raise

def evaluate_model(coin: str) -> dict:
    """Evaluate model with multiple metrics"""
    try:

        X_train, X_test, y_train, y_test = split_data(coin)
        model_path = os.path.join(DATA_PATHS['model'], f"{coin}_weights.pkl")
        model =joblib.load(model_path)
        predictions = model.predict(X_test)
        metrics = {
                'coin': coin,
                'mse': mean_squared_error(y_test, predictions),
                'r2': r2_score(y_test, predictions),
                'mae': mean_absolute_error(y_test, predictions),
                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            }
        
        logger.info(f"model performance for {coin}: {metrics}")

        metrics_path = os.path.join(DATA_PATHS['model'],f"{coin}_metrics.csv")

        df_metrics = pd.DataFrame([metrics])
        if not os.path.exists(metrics_path):
            df_metrics.to_csv(metrics_path, index=False)
        else:
            df_metrics.to_csv(metrics_path, mode='a', header=False, index=False)
        return metrics
    
    except Exception as e:
        logger.error(f"measuring the performace of the model is failed {str(e)}")
        raise

