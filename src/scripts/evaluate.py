from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import pandas as pd
import sys
from utils.logger import get_logger
from scripts.model import prepare_data
logger = get_logger('model')

def evaluate_model(model, X_test, y_test) -> dict:
    """Evaluate model with multiple metrics"""
    try:
        predictions = model.predict(X_test)
        metrics = {
            'mse': mean_squared_error(y_test, predictions),
            'r2': r2_score(y_test, predictions),
            'mae': mean_absolute_error(y_test, predictions)
        }
        logger.info(f"Model metrics: MSE={metrics['mse']:.4f}, R2={metrics['r2']:.4f}, MAE={metrics['mae']:.4f}")
        return metrics
    except Exception as e:
        logger.error(f"Error evaluating model: {str(e)}")
        raise

if __name__ == "__main__":
    model_path = sys.argv[1]
    data_path = sys.argv[2]

    model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    _, X_test, _, y_test = prepare_data(df)
    evaluate_model(model, X_test, y_test)