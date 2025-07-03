"""Main entry point for CryptoPredictor Flask app"""

from flask import Flask, request
from config.config import config
from utils.logger import get_logger
from api.routes import main_bp
import os

logger = get_logger("app")


def create_app(config_name="default") -> Flask:
    """Create and configure Flask application"""
    cfg = config[config_name]
    app = Flask(__name__, template_folder="templates", static_folder="static")
    # Load class-based configuration
    app.config.from_object(cfg)

    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method}{request.path}")

    app.register_blueprint(main_bp)
    return app


if __name__ == "__main__":
    config_name = os.getenv("APP_ENV", "default")
    app = create_app(config_name)
    app.run(host=config["default"].HOST, port=config["default"].PORT)
