"""Builds and trains ML model."""
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
import os
from pathlib import Path
import joblib 
import psycopg2
import pandas as pd
from typing import Optional
from datetime import datetime
from airflow.exceptions import AirflowFailException
from utils.logger import get_logger
from config.config import DB_CONFIG, DATA_PATHS
from utils.helper import get_db_connection

logger = get_logger('model')

def prepare_data(df: pd.DataFrame):
    """Prepare features and target, and perform train-test split"""
    try:
        X = df[[
            'lag_1', 'lag_2', 'lag_3', 'lag_7', 'lag_14',
            'rolling_mean_3', 'rolling_std_3', 
            'rolling_mean_7', 'rolling_std_7',
            'rolling_max_7', 'rolling_min_7',
            'price_diff', 'pct_change_1', 'pct_change_7',
            'day_of_week', 'day_of_month', 'month', 'is_weekend',
            'exp_moving_avg_10', 'volatility_10'
        ]]
        y = df['target']

         # Time-based train-test split (last 20% as test)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        logger.info("Data prepared and splited into training and test sets")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(f"Error in data preparation: {str(e)}")
        raise

   
def train_model(coin:str, hyperparams: dict = None):
    """Train a Random Forest model with grid search"""
    table_name = f'model_weights_{coin}'
    raw_table = f'extract_features_{coin}'

    try:
        with get_db_connection(DB_CONFIG) as conn:
            query = f"SELECT * FROM  {raw_table}"
            df = pd.read_sql(query, conn)
            logger.info(f"Loaded data sucessfully from {raw_table}")
    except Exception as e:
        logger.error(f"Load data from {coin}: is failed{str(e)}")
        raise
    
    if df.empty:
        logger.warning(f"No data for this {coin}")
        return None
      
    X_train, X_test, y_train, y_test = prepare_data(df)

    # Train the model
    model = RandomForestRegressor(random_state=42)
    if hyperparams:
        tscv = TimeSeriesSplit(n_splits=3)
        grid_search = GridSearchCV(estimator=model, param_grid=hyperparams, scoring='neg_mean_absolute_error', cv=tscv, n_jobs=-1)
        grid_search.fit(X_train, y_train)
        model = grid_search.best_estimator_
        logger.info(f"Best hyperparameters for {coin} : {grid_search.best_estimator_}")
    else:
        model.fit(X_train, y_train)
        logger.info(f"Trained new model for {coin}")

    model_path = os.path.join(DATA_PATHS['model'],f"{coin}_weights.pkl")
    
    joblib.dump(model, model_path)
    logger.info(f"Saved initial model for {coin} at: {model_path}")
