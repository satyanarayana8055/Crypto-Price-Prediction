"""Tests for ML model"""
import pytest
import os
import pandas as pd
from scripts.model import train_model
from config.config import DATA_PATHS

def test_model_prediction():
    """Test model prediction"""
    df = pd.read_csv(os.path.join(DATA_PATHS['processed'],'bitcoin_transformed.csv'))
    model, X_test, y_test = train_model(df, 'bitcoin')
    predictions = model.predict(X_test)
    assert len(predictions) == len(y_test), "Prediction length mismatch" 
    assert all(pred >=0 for pred in predictions), "Negative prediction detected"

if __name__ == "__main__":
    pytest.main()