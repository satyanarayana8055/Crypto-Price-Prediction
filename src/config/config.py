"""
The config.py file acts as a central controller for the project, storing all directory paths, file locations, 
and configurable parameters. It enables easier parameter tuning and promotes modular, maintainable code
"""
import os 
from dotenv import load_dotenv
from pathlib import Path

# It is the base folder to get access from outside the src folder 
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR /'.env')

def validate_env_vars():
    """Validate required environment variables"""
    required_vars = ['DB_USER','DB_PASSWORD','DB_HOST','DB_PORT','DB_NAME','FLASK_SECRET_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"Missing enviroment variables: {missing}")
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
# Log configuration
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL','INFO'),
    'max_bytes':int(os.getenv('LOG_MAX_BYTES',10485760)),
    'backup_count': int(os.getenv('LOG_BACKUP',5))
}

# Data paths
DATA_PATHS = {
    'raw': Path('/app/data/raw'),
    'processed': Path('/app/data/processed'),
    'extract': Path('/app/data/extract'),
    'model_weight': Path ('/app/data/model/weight'),
    'model_metrics': Path ('/app/data/model/metrics'),
    'drift_html': Path('/app/data/monitor/drift'),
    'perform_metrics': Path('/app/data/monitor/performance/')
    
    # 'model': BASE_DIR / 'data' / 'model'
}


THRESHOLDS = {
    'mae': os.getenv('MAE'),
    'mse': os.getenv('MSE'),
    'r2' : os.getenv('R2')
}

print("Configuration loaded successfully")
