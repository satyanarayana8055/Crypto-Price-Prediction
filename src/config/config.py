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
    required_vars = ['DB_USER','DB_PASSWORD','DB_HOST','DB_PORT','DB_NAME']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"Missing enviroment variables: {missing}")
        raise ValueError(f"Missing enviroment variables:{missing}")
    
validate_env_vars()

# Package constants 
# For code flexibilty we can add any coin name without changing src code and it create the table for it
PACKAGE_NAME = "cryptoPredictor"
COINS = os.getenv('COINGECKO_COINS','bitcoin').split(',')
COINS = [coin.strip() for coin in COINS]  
TABLE_NAME = {coin: f"{coin}_prices" for coin in COINS}

# Database configuration
DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

# Database configuration
DB_API_CONFIG = {
    'user': os.getenv('API_USER'),
    'password': os.getenv('API_PASSWORD'),
    'host': os.getenv('API_HOST'),
    'port': os.getenv('API_PORT'),
    'database': os.getenv('API_NAME')
}

# Log configuration
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL','INFO'),
    'max_bytes':int(os.getenv('LOG_MAX_BYTES',10485760)),
    'backup_count': int(os.getenv('LOG_BACKUP',5))
}

# Data paths
DATA_PATHS = {
    'raw': BASE_DIR / 'data' / 'raw',
    'transfrom': BASE_DIR / 'data' / 'transfrom',
    'processed': BASE_DIR / 'data' / 'processed',
    'model_weight': BASE_DIR / 'data' / 'model' / 'weight',
    'model_metrics': BASE_DIR / 'data' / 'model' / 'metrics',
    'drift_html': BASE_DIR / 'data' / 'monitor' / 'drift',
    'perform_metrics': BASE_DIR / 'data' / 'monitor' / 'performance'
}

THRESHOLDS = {
    'mae': os.getenv('MAE'),
    'mse': os.getenv('MSE'),
    'r2' : os.getenv('R2')
}

class Web:
    "WEB base configuration class"

    # Flask settings 
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or 'crypto-predict-secret-key-2025'
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))

    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH')
    CACHE_DURATION = os.getenv('CACHE_DURATION')
    
    # Email settings for notifications
    SMTP_SERVER = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    SMTP_PORT = os.getenv('EMAIL_PORT', 587)
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')
    
    # API settings 
    COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
    COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 10))
 
    # Cache settings
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 300))

    # Security settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

class DevelopementConfig(Web):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Web):
    """Production configuration"""
    DEBUG = True

class TestingConfig(Web):
    """Production configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'

# Configuration dictionary
config = {
    'development': DevelopementConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopementConfig
}

print("Configuration loaded successfully")

