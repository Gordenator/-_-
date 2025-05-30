import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tihaya_gavan.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False