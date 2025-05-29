"""Main entry point for CryptoPredictor Flask app"""
from flask import Flask
from flask_caching import Cache
from config.config import FLASK_CONFIG
from utils.logger import get_logger
from app.routes import init_routes
from flask import Flask, request

logger = get_logger('app')

def create_app() -> Flask:
    """Create and configure Flask application"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = FLASK_CONFIG['secret_key']
    app.config['DEBUG'] = FLASK_CONFIG['debug']
    cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': FLASK_CONFIG['cache_timeout']})
   
    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method}{request.path}")
      
    init_routes(app, cache)
    logger.info("Flask application initialized")
    return app
     
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)