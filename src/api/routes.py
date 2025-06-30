"""API endpoints for CryptoPredictor Flask app"""
from flask import Blueprint, render_template, jsonify, request
from services.data_service import DataService
from services.model_service import ModelService
from utils.logger import get_logger
from config.config import DATA_PATHS
import os

logger = get_logger('app')

main_bp = Blueprint('main', __name__) 

# Initialize services
data_service = DataService()
model_service = ModelService()


@main_bp.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@main_bp.route('/prediction')
def prediction():
    """Prediction page route"""
    return render_template('prediction.html')

@main_bp.route('/data-drift')
def data_drift():
    """Data drift monitoring page"""
    return render_template('data_drift.html')

@main_bp.route('/alerts')
def alerts():
    """Alerts configuration page"""
    return render_template('alerts.html')

@main_bp.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')

# API Routes
@main_bp.route('/api/data/<coin_id>')
def get_coin_data(coin_id):
    """Get live data for specific coin"""
    try:
        data = data_service.get_live_data(coin_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/historical/<coin_id>')
def get_historical_data(coin_id):
    """Get historical data for charts"""
    try:
        days = request.args.get('days', 30, type=int)
        data = data_service.get_historical_data(coin_id, days)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/coins')
def get_supported_coins():
    """Get list of supported coins"""
    try:
        coins = data_service.get_supported_coins()
        return jsonify(coins)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/predict/<coin_id>')
def predict_price(coin_id):
    """Get price prediction"""
    try:
        prediction = model_service.predict(coin_id)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/model-metrics/<coin_id>')
def get_model_metrics(coin_id):
    """Get model performance metrics"""
    try:
        metrics = model_service.get_metrics(coin_id)
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@main_bp.route('/api/drift/<coin_id>')
def get_drift_data(coin_id):
    """Get data drift information"""
    try:
        # Check if drift HTML files exists
        drift_file = os.path.join(DATA_PATHS['drift_html'],f"{coin_id}_drift_report.html")
        if os.path.exists(drift_file):
            with open(drift_file, 'r') as f:
                html_content = f.read()
            return html_content
        else:
            return jsonify({'error': 'Drift report not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    

    
# @main_bp.route('/coins')
# def get_coins():
#     """Get list of available coins"""
#     try:
#         coins = data_service.get_available_coins()
#         return jsonify({'success': True, 'data': coins})
#     except Exception as e:
#         logger.error(f"Error fetching coins: {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500
# @main_bp.route('/data/<coin_id>')
# def get_coin_data(coin_id):
#     """Get current coin data"""
#     try:
#         data = data_service.get_coin_data(coin_id)
#         return jsonify({'success': True, 'data': data})
#     except Exception as e:
#         logger.error(f"Error fetching coin data fro {coin_id}: {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500
    
# @main_bp.route('/predict/<coin_id>')
# def predict_price(coin_id):
#     """Get price prediction for coin"""
#     try:
#         prediction = model_service.predict(coin_id)
#         return jsonify({'success': True, 'data': prediction})
#     except Exception as e:
#         logger.error(f"Error predicting price for {coin_id}: {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500
    
# @main_bp.route('/metrics/<coin_id>')
# def get_metrics(coin_id):
#     """Get model performance metrics"""
#     try:
#         metrics = model_service.get_performance_metrics(coin_id)
#         return jsonify({'success': True, 'data': metrics})
#     except Exception as e:
#         logger.error(f"Error fetchingg metrics for {coin_id}: {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500

# @main_bp.route('/historical/<coin_id>')
# def get_historical_data(coin_id):
#     """Get historical price data"""
#     try:
#         days = request.args.get('days', 30, type=int) 
#         data = data_service.get_historical_data(coin_id, days)
#         return jsonify({'success': True, 'data': data})
#     except Exception as e:
#         logger.error(f"Error fetching historical data for {coin_id}: {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500
    
