from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os
import re
import joblib
import pandas as pd
import mlflow
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
    
    _, X_test, _, y_test = split_data(coin)
    model_dir = DATA_PATHS['model_weight']
    model_files = sorted(model_dir.glob(f"{coin}_weight_*.pkl"))
    metrics_path = os.path.join(DATA_PATHS['model_metrics'],f"{coin}_metrics.csv")

    if not model_files:
        logger.warning(f"No versioned models found for {coin} in {model_dir}")
        return 
    
    # Prepare fresh results
    results = []
    
    for model_file in model_files:
        try:
            model =joblib.load(model_file)
            predictions = model.predict(X_test)
        
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)
            mae = mean_absolute_error(y_test, predictions)
            metrics = {
                    'name': model_file.name,
                    'coin': coin,
                    'mse': mse,
                    'r2': r2,
                    'mae': mae,
                    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                }
            results.append(metrics)
            logger.info(f"Evaluated {model_file.name} — R2: {r2:.4f}, MSE: {mse:.4f}, MAE: {mae:.4f}")

        except Exception as e:
            logger.error(f"measuring the performace of the model is failed {str(e)}")

  
    # Save ONLY latest evaluation results (overwrite)
    df_metrics = pd.DataFrame(results)
    df_metrics.to_csv(metrics_path, index=False)
    logger.info(f"Evaluation metrics saved to {metrics_path}")
