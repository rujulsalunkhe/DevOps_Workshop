import os
from pathlib import Path

class Config:
    """Application configuration"""
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = ENV == 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    BASE_DIR = Path(__file__).parent.parent
    DATABASE_PATH = os.environ.get('DATABASE_PATH', str(BASE_DIR / 'data.db'))
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', str(BASE_DIR / 'app.log'))
