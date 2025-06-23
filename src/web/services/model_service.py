"""Model prediction service for CrytoPredictor"""
import joblib 
import pandas as pd
import glob
import os
from utils.logger import get_logger
from config.config import DATA_PATHS

logger = get_logger('model_service')

def predict_price(coin: str) -> float:
    """Predict price for a coin"""
    try:
        model_path = os.path.join(DATA_PATHS['model'], f'{coin}_model.pkl')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model for {coin} not found")
        model = joblib.load(model_path)
        latest_file = sorted(glob.glob(os.path.join(DATA_PATHS['transformed'], f'{coin}_transformed.csv')))[-1]
        df = pd.read_csv(latest_file)
        features = df[['ma_7', 'ma_14', 'lag_price_1', 'lag_price_2', 'lag_return_1', 'return_ma_ratio_7', 'return_ma_ratio_14', 'price_volatility_7']].iloc[[-1]]
        prediction = model.predict(features)[0]
        logger.info(f"Predicted price for {coin}: {prediction}")
        return prediction
    except Exception as e:
        logger.error(f"Error predicting price for {coin}: {str(e)}")
        raise