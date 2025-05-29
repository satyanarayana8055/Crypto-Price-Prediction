"""API endpoints for CryptoPredictor Flask app"""
from flask import render_template, jsonify, request
from app_services.model_service import predict_price
from app_services.data_service import get_latest_data
from utils.logger import get_logger
from config.config import COINGECKO_CONFIG, FLASK_CONFIG
from functools import wraps

logger = get_logger('app')

def validate_coin(f):
    """Decorator to validate coin parameter"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        coin = request.args.get('coin', 'bitcoin')
        if coin not in COINGECKO_CONFIG['coins']:
            logger.error(f"Invalid coin: {coin}")
            return jsonify({'error': f"Invalid coin: {coin}"}), 400
        return f(coin, *args, **kwargs)
    return decorated_function

def init_routes(app, cache):
    """Initialize Flask routes"""
    @app.route('/')
    def home():
        logger.info("Accessed home page")
        return render_template('index.html')
    @app.route('/predict')
    @validate_coin
    @cache.cached(timeout=FLASK_CONFIG['cache_timeout'])
    def predict(coin):
        try:
            prediction = predict_price(coin)
            logger.info(f"Generated prediction for {coin}: {prediction}")
            return jsonify({'coin': coin, 'prediction': prediction})
        except Exception as e:
            logger.error(f"Error predicting for {coin}: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
    @app.route('/data')
    @validate_coin
    def data(coin):
        try:
            latest_data = get_latest_data(coin)
            logger.info(f"Fetched latest data for {coin}")
            return jsonify(latest_data)
        except Exception as e:
            logger.error(f"Error  fetching data for {coin}: {str(e)}")
            return jsonify({'error': str(e)}), 500