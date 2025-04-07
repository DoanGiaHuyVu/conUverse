from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Import models AFTER db initialization
    from . import models
    
    # Initialize database within app context
    with app.app_context():
        from .test_data import init_test_data
        init_test_data()
    
    from .routes import init_routes
    init_routes(app)
    
    return app