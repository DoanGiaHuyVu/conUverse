import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'  # Change this in production!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///social_media.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False