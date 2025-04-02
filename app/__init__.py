from flask import Flask
from flask_mysqldb import MySQL
from app.config import Config  # Add this import at the top

mysql = MySQL()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize MySQL
    mysql.init_app(app)
    
    # Register blueprints (routes)
    from app.routes import main
    app.register_blueprint(main)
    
    return app