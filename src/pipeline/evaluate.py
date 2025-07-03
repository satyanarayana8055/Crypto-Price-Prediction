from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os
import re
import joblib
import glob
import pandas as pd
import numpy as np
from utils.logger import get_logger
from config.config import DB_CONFIG, DATA_PATHS
from pipeline.model import prepare_data
from utils.helper import get_db_connection, ensure_directory

logger = get_logger("model")


def split_data(coin: str):
    table_name = f"extract_features_{coin}"

    try:
        with get_db_connection(DB_CONFIG) as conn:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)

            return prepare_data(df)

    except Exception as e:
        logger.error(f"failed to split the {str(e)}")
        raise


def best_metrics(df: pd.DataFrame, coin: str) -> pd.DataFrame:

    # Get the row with the best R² score
    best_metrics = df.loc[df["accuracy"].idxmax()]
    best_metrics_df = best_metrics.to_frame().T

    # Path for performance metrics file
    metrics_file = os.path.join(
        DATA_PATHS["perform_metrics"], f"{coin}_performance_metrics.csv"
    )

    # If file exists, append without header; otherwise, write with header
    if os.path.exists(metrics_file):
        best_metrics_df.to_csv(metrics_file, mode="a", index=False, header=False)
    else:
        best_metrics_df.to_csv(metrics_file, index=False, header=True)

    # Load the best model using its name
    best_weight_name = best_metrics_df["name"].values[0]
    model_path = os.path.join(DATA_PATHS["model_weight"], best_weight_name)

    # Ensure best_model directory exists
    ensure_directory(DATA_PATHS["best_model"])

    # Deleting every thing before inserting new weights
    for file in glob.glob(os.path.join(DATA_PATHS["best_model"], "*")):
        os.remove(file)

    # Save the best model
    best_model_path = os.path.join(DATA_PATHS["best_model"], best_weight_name)
    best_model = joblib.load(model_path)
    joblib.dump(best_model, best_model_path)


def mean_absolute_percentage_error(y_true, y_pred):
    """Custom MAPE implementation (sklearn doesn't have built-in MAPE)"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero = y_true != 0
    mape = (
        np.mean(np.abs((y_true[non_zero] - y_pred[non_zero]) / y_true[non_zero])) * 100
    )
    return mape


def evaluate_model(coin: str) -> dict:
    """Evaluate model with multiple metrics"""

    def extract_weight_number(path_obj):
        match = re.search(rf"{coin}_weight_(\d+)\.pkl", path_obj.name)
        return int(match.group(1)) if match else float("inf")

    _, X_test, _, y_test = split_data(coin)
    model_dir = DATA_PATHS["model_weight"]
    model_files = sorted(
        model_dir.glob(f"{coin}_weight_*.pkl"), key=extract_weight_number
    )
    metrics_path = os.path.join(DATA_PATHS["model_metrics"], f"{coin}_metrics.csv")

    if not model_files:
        logger.warning(f"No versioned models found for {coin} in {model_dir}")
        return

    # Prepare fresh results
    results = []

    for model_file in model_files:
        try:
            model = joblib.load(model_file)
            predictions = model.predict(X_test)

            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions) * 100
            mae = mean_absolute_error(y_test, predictions)
            mape = mean_absolute_percentage_error(y_test, predictions)
            metrics = {
                "name": model_file.name,
                "coin": coin,
                "mse": mse,
                "mape": mape,
                "accuracy": r2,
                "mae": mae,
                "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            }
            results.append(metrics)
            logger.info(
                (
                    f"Evaluated {model_file.name} — "
                    f"R2: {r2:.4f}, MSE: {mse:.4f}, MAE: {mae:.4f}"
                ),
            )

        except Exception as e:
            logger.error(f"measuring the performace of the model is failed {str(e)}")

    # Save ONLY latest evaluation results (overwrite)
    df_metrics = pd.DataFrame(results)
    df_metrics.to_csv(metrics_path, index=False)
    logger.info(f"Evaluation metrics saved to {metrics_path}")
    best_metrics(df_metrics, coin)
    logger.info("In that metrics best metrics also save to csv")
