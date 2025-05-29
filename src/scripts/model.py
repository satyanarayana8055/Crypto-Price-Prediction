"""Builds and trains ML model."""
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
import joblib 
import pandas as pd
import os
import sys
from utils.logger import get_logger
from config.config import DATA_PATHS
from utils.helper import ensure_directory

logger = get_logger('model')

def prepare_data(df: pd.DataFrame):
    """Prepare features and target, and perform train-test split"""
    try:
         X = df[['ma_7', 'ma_14', 'lag_price_1', 'lag_price_2', 'lag_return_1', 'return_ma_ratio_7', 'return_ma_ratio_14', 'price_volatility_7']]
         y = df['price']
         # Time-based train-test split (last 20% as test)
         split_idx = int(len(X) * 0.8)
         X_train, X_test = X[:split_idx], X[split_idx:]
         y_train, y_test = y[:split_idx], y[split_idx:]
         logger.info("Data prepare d and splited into training and test sets")
         return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(f"Error in data preparation: {str(e)}")
        raise
    
def train_model(X_train, X_test, y_train, y_test, coin: str, hyperparams: dict = None) -> tuple:
    """Train a Random Forest model with grid search"""
    try:
        model = RandomForestRegressor(random_state=42)
        if hyperparams:
            tscv = TimeSeriesSplit(n_splits=5)
            grid_search = GridSearchCV(estimator=model, param_grid=hyperparams, scoring='neg_mean_absolute_error', cv=tscv, n_jobs=-1, verbose=2)
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
            logger.info(f"Best hyperparameter for {coin}: {grid_search.best_params_}")
        else:
            model.fit(X_train, y_train)
        model_path = os.path.join(DATA_PATHS['model'], f'{coin}_model.pkl')
        ensure_directory('models')
        joblib.dump(model, model_path)
        logger.info(f"Model for {coin} saved to {model_path}")

        return model, X_test, y_test
    except Exception as e:
        logger.error(f"Error training model for {coin}: {str(e)}")
        raise

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    coin = sys.argv[2]
    hyperparams = {
        'n_estimators': [50, 100, 150, 200],
        'max_depth': [None, 5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', 0.5],
    }
    X_train, X_test, y_train, y_test = prepare_data(df) 
    model=train_model(X_train, X_test, y_train, y_test, coin, hyperparams)