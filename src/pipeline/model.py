"""Builds and trains ML model."""
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
import joblib 
import mlflow
import mlflow.sklearn
import pandas as pd
from itertools import product
from utils.logger import get_logger
from config.config import DB_CONFIG, DATA_PATHS
from utils.helper import get_db_connection

logger = get_logger('model')

def prepare_data(df: pd.DataFrame):
    """Prepare features and target, and perform train-test split"""
    try:
        df = df.dropna().reset_index(drop=True)
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

    mlflow.set_tracking_uri("http://mlflow:5001")  
    mlflow.set_experiment(f"{coin}-training")

    param_grid = {
        "n_estimators": hyperparams.get("n_estimators", [100]),
        "max_depth": hyperparams.get("max_depth",[None]),
        "min_samples_split": hyperparams.get("min_samples_split",[2]),
        "min_samples_leaf": hyperparams.get("min_samples_leaf",[1]),
        "max_features": hyperparams.get("max_features",["sqrt"]),
    }
    combinations = list(product(
        param_grid["n_estimators"],
        param_grid["max_depth"],
        param_grid["min_samples_split"],
        param_grid["min_samples_leaf"],
        param_grid["max_features"]
    ))
    
    for i, (n_est, depth, split, leaf, feat) in enumerate(combinations, start=1):
    # Train the model
        try:
            with mlflow.start_run(run_name=f"{coin}_training_run_{i}"):
                mlflow.log_param("n_estimators", n_est)
                mlflow.log_param("max_depth", depth)
                mlflow.log_param("min_samples_split", split)
                mlflow.log_param("min_samples_leaf", leaf)
                mlflow.log_param("max_features", feat)

                model = RandomForestRegressor(n_estimators=n_est, max_depth=depth, min_samples_split=split, min_samples_leaf=leaf, max_features=feat, random_state=42)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_train)
                mlflow.log_metric("train_mse", mean_squared_error(y_train, y_pred))
                mlflow.log_metric("train_r2", r2_score(y_train, y_pred))
                mlflow.log_metric("train_mae", mean_absolute_error(y_train, y_pred))
            
                yt_pred = model.predict(X_test)
                mlflow.log_metric("test_mse", mean_squared_error(y_test, yt_pred))
                mlflow.log_metric("test_r2", r2_score(y_test, yt_pred))
                mlflow.log_metric("test_mae", mean_absolute_error(y_test,yt_pred))

                # save the model locally
                model_path = os.path.join(DATA_PATHS['model_weight'], f"{coin}_weight_{i}.pkl")
                joblib.dump(model,model_path)
                logger.info(f"Saved model for {coin} at {model_path}")
                
                # Log to MLflow
                mlflow.sklearn.log_model(model, artifact_path="model")
        except Exception as e:
            logger.error(f"Model train with mlflow is failed due to {i}: {str(e)}")
 
