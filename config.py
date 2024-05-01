# config.py

import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    username = '...'
    password = '...'

    # Escape username and password according to RFC 3986
    escaped_username = quote_plus(username)
    escaped_password = quote_plus(password)
    
    MONGO_URI = f'mongodb+srv://{escaped_username}:{escaped_password}@cluster0.gk7frvp.mongodb.net/'
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit for uploaded files




