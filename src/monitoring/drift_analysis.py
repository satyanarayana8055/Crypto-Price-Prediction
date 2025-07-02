from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.pipeline.column_mapping import ColumnMapping
from utils.logger import get_logger
from utils.helper import get_db_connection, ensure_directory
from config.config import DB_CONFIG, DATA_PATHS
import pandas as pd
import os

logger = get_logger("monitor")


def get_drift(
    reference_data: pd.DataFrame, current_data: pd.DataFrame, coin: str
) -> dict:
    """Analyze data drift for a coin"""
    try:
        # columnmapping tells which column is numerical
        column_mapping = ColumnMapping(
            numerical_features=[
                "lag_1",
                "lag_2",
                "rolling_mean_7",
                "rolling_std_7",
                "price_diff",
                "pct_change_1",
                "pct_change_7",
                "day_of_week",
                "month",
                "is_weekend",
                "exp_moving_avg_10",
                "volatility_10",
            ]
        )
        # Report help initialize the report and datadriftpresent help
        # to check each feature drift
        report = Report(metrics=[DataDriftPreset()])
        report.run(
            reference_data=reference_data,
            current_data=current_data,
            column_mapping=column_mapping,
        )

        # It is used to make it as dictionary and drift_detected check weather
        # dict structure is as need or not
        result_dict = report.as_dict()
        drift_detected = result_dict["metrics"][0]["result"]["dataset_drift"]

        # Save HTML report
        output_dir = os.path.join(DATA_PATHS["drift_html"])
        ensure_directory(output_dir)
        output_path = os.path.join(output_dir, f"{coin}_drift_report.html")
        logger.info(f"Data drift for {coin}: {drift_detected}")
        report.save_html(output_path)
        return {
            "coin": coin,
            "drift_detected": drift_detected,
            "details": result_dict}

    except Exception as e:
        logger.error(f"Error analyzing drift for {coin}: {str(e)}")
        raise


def analyze_drift(coin: str) -> pd.DataFrame:
    try:
        with get_db_connection(DB_CONFIG) as conn:
            query = f"SELECT * FROM extract_features_{coin}"
            df = pd.read_sql(query, conn)
    except Exception as e:
        logger.error(f"Load data from {coin}: is failed{str(e)}")
        raise

    if df.empty:
        logger.warning(f"No data for this {coin}")
        return None

    drift_df = df[
        [
            "lag_1",
            "lag_2",
            "rolling_mean_7",
            "rolling_std_7",
            "price_diff",
            "pct_change_1",
            "pct_change_7",
            "day_of_week",
            "month",
            "is_weekend",
            "exp_moving_avg_10",
            "volatility_10",
        ]
    ]
    split_idx = len(drift_df) // 2
    reference_data = drift_df.iloc[:split_idx]
    current_data = drift_df.iloc[split_idx:]

    return get_drift(reference_data, current_data, coin)
