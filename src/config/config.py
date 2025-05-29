"""
The config.py file acts as a central controller for the project, storing all directory paths, file locations, 
and configurable parameters. It enables easier parameter tuning and promotes modular, maintainable code
"""
import os 
from dotenv import load_dotenv
from utils.logger import get_logger
from pathlib import Path

# It is the base folder to get access from outside the src folder 
BASE_DIR = Path(__file__).resolve().parent.parent.parent
logger = get_logger('etl')

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR /'.env')

def validate_env_vars():
    """Validate required environment variables"""
    required_vars = ['DB_USER','DB_PASSWORD','DB_HOST','DB_PORT','DB_NAME','FLASK_SECRET_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.error(f"Missing enviroment variables: {missing}")
        raise ValueError(f"Missing enviroment variables:{missing}")
    
validate_env_vars()

# Package constants 
# For code flexibilty we can add any coin name without changing src code and it create the table for it
PACKAGE_NAME = "cryptoPredictor"
COINS = os.getenv('COINGECKO_COINS','bitcoin').split(',')
TABLE_NAME = {coin: f"{coin}_prices" for coin in COINS}

# Database configuration
DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

# Flask configuration
FLASK_CONFIG = {
    'secret_key': os.getenv('FLASK_SECRET_KEY',None), # It get values from .env if not the default values are given to maintain clean and error prevention
    'debug': os.getenv('FLASK_ENV', 'development') == 'development', # In this also defalut value if value is equals then debug is True not Debug is False it is for developement and production
    'cache_timeout': 300
 }

# CoinGecko API configuration
COINGECKO_CONFIG = {
    'api_key': os.getenv('COINGECKO_API_KEY', None),
    'base_url': 'https://api.coingecko.com/api/v3',
    'coins': COINS
}

# Email configuration
EMAIL_CONFIG = {
    'host': os.getenv('EMAIL_HOST', 'smtp.gmail.com'),
    'port': os.getenv('EMAIL_PORT',587),
    'user': os.getenv('EMAIL_USER'),
    'password': os.getenv('EMAIL_PASSWORD')
}

# Data paths
DATA_PATHS = {
    'raw': BASE_DIR/'data'/'raw',
    'processed': BASE_DIR/'data'/'processed',
    'transformed': BASE_DIR/'data'/'model'/'feature_extraction',
    'model':BASE_DIR/'data'/'model/weights'
}

logger.info("Configuration loaded successfully")
