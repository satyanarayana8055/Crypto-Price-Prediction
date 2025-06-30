"""Tracks model performance metrics"""
import pandas as pd
import os
import sys
import mlflow
import requests
from utils.logger import get_logger
from config.config import DATA_PATHS

logger = get_logger('monitor')


def monitor_metrics(coin: str):

    path = os.path.join(DATA_PATHS['model_metrics'],f"{coin}_metrics.csv")
    df = pd.read_csv(path)
    
    # Get the row with the best R² score
    best_metrics = df.loc[df['accuracy'].idxmax()]
    best_metrics_df=best_metrics.to_frame().T

    # Path for performance metrics file
    output_path = os.path.join(DATA_PATHS['perform_metrics'],f"{coin}_performance_metrics.csv")

    # If file exists, append without header; otherwise, write with header
    if os.path.exists(output_path):
        best_metrics_df.to_csv(output_path, mode='a', index=False, header=False)
    else:
        best_metrics_df.to_csv(output_path, index=False, header=True)


# def monitor_metrics(coin: str):


    # # Compare with thresholds
    # alerts = []
    # if mae > THRESHOLDS["mae"]:
    #     alerts.append(f"MAE too high: {mae:.3f} > {THRESHOLDS['mae']}")

    # if mse > THRESHOLDS["mse"]:
    #     alerts.append(f"Accuracy too low: {mse:.3f} < {THRESHOLDS['mse']}")
        
    # if r2 < THRESHOLDS["r2"]:
    #     alerts.append(f"r2 too low: {r2:.3f} < {THRESHOLDS['r2']}")

    # # Send alerts if needed
    # if alerts:
    #     message = "\n".join(alerts)
    #     send_alert(message)
    # else:
    #     print(f"Model performance is within acceptable limits")
    


