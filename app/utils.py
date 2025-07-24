import logging
import re
from app.config import Config

def setup_logging():
    """Setup application logging"""
    config = Config()
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def validate_user_data(data):
    """Validate user input data"""
    if not data:
        return "No data provided"
    
    if 'name' not in data or not data['name']:
        return "Name is required"
    
    if 'email' not in data or not data['email']:
        return "Email is required"
    
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        return "Invalid email format"
    
    # Name length validation
    if len(data['name']) < 2 or len(data['name']) > 50:
        return "Name must be between 2 and 50 characters"
    
    return None
