"""Tests for ML model"""

import pytest
import os
import numpy as np
import pandas as pd
import joblib
from config.config import DATA_PATHS, COINS
from pipeline.model import prepare_data


@pytest.mark.parametrize("coin", COINS)
def test_model_prediction(coin):
    """Test model prediction for each coin"""
    features_path = os.path.join(
        DATA_PATHS["extracted"], f"extracted_features_{coin}.csv"
    )
    df = pd.read_csv(features_path)

    assert not df.empty, f"Loaded data is empty for coin: {coin}"

    _, X_test, _, y_test = prepare_data(df)

    # Load best model info
    perf_path = os.path.join(
        DATA_PATHS["performance_metrics"], f"{coin}_performance_metrics.csv"
    )
    assert os.path.exists(perf_path), f"Performance metrics not found: {perf_path}"

    best_model_df = pd.read_csv(perf_path)
    assert not best_model_df.empty, f"No performance data for: {coin}"

    best_model_name = best_model_df["name"].iloc[-1]
    model_path = os.path.join(DATA_PATHS["best_model"], best_model_name)
    assert os.path.exists(model_path), f"Model file not found: {model_path}"

    model = joblib.load(model_path)

    # Model predictions
    predictions = model.predict(X_test)

    # Prediction shape test
    assert len(predictions) == len(y_test), "Prediction length mismatch"

    # Negative prediction test
    assert all(pred >= 0 for pred in predictions), "Negative prediction detected"

    # Prediction output type test
    assert isinstance(
        predictions[0], (float, int, np.float64, np.float32)
    ), "Prediction is not numeric"
