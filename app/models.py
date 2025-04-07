import uuid
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'user'  # Explicit table name

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(100))
    posts = db.relationship('Post', backref='author', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def generate_token(self, expires_in=3600):
        return jwt.encode(
            {'public_id': self.public_id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            'your-secret-key',  # Change this to a secure secret
            algorithm='HS256'
        )
    
    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            return data['public_id']
        except:
            return None

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)