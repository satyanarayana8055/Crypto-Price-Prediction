from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.pipeline.column_mapping import ColumnMapping
from utils.logger import get_logger
import pandas as pd
import sys

logger = get_logger('monitor')

def analyze_drift(reference_data: pd.DataFrame, current_data: pd.DataFrame, coin: str) -> dict:
    """Analyze data drift for a coin"""
    try:
        column_mapping = ColumnMapping(numerical_features=['price','daily_return', 'ma_7', 'ma_14'])
        
        # Create a drift report
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

        # Convert the report to a dictionary
        result_dict = report.as_dict()
        drift_detected = result_dict["metrics"][0]["result"]["dataset_drift"]
        logger.info(f"Data drift for {coin}: {drift_detected}")
        return {'coin': coin, 'drift_detected': drift_detected, 'details': result_dict}
    except Exception as e:
        logger.error(f"Error analyzing drift for {coin}: {str(e)}")
        raise

if __name__ == "__main__":
    reference_data = pd.read_csv(sys.argv[1])
    current_data = pd.read_csv(sys.argv[2])
    coin = sys.argv[3]
    analyze_drift(reference_data, current_data, coin)