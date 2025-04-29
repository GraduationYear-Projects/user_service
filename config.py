import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI')
    MONGODB_DB = os.getenv('MONGODB_DB')
    
    # Flask Configuration
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    FLASK_HOST = os.getenv('FLASK_HOST')
    FLASK_PORT = os.getenv('FLASK_PORT')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY') 