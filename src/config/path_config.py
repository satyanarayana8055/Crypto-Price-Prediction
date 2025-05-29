"""It contains some path that causes cyclic issuse in config.py and helper.py & logger.py file"""
import os 
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Logging configuration

# It is the base folder to get access from outside the src folder 
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv()

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR /'.env')

LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL','INFO'),
    'max_bytes':int(os.getenv('LOG_MAX_BYTES',10485760)),
    'backup_count': int(os.getenv('LOG_BACKUP',5))
}

DATA_PATHS = {
    'raw': BASE_DIR/'data'/'raw',
    'processed': BASE_DIR/'data'/'processed',
    'model':BASE_DIR/'data'/'model'
    }