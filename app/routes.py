from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Post
import uuid
import datetime
from functools import wraps

def init_routes(app):
    # ========================
    # Authentication Routes
    # ========================
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
            
        user = User(
            email=data['email'],
            username=data['username'],
            password=data['password']  # In production, you should hash this
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'username': user.username
        })

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(
            email=data['email'],
            password=data['password']  # Plaintext comparison for prototype
        ).first()
        
        if user:
            return jsonify({
                'success': True,
                'user_id': user.id,
                'username': user.username
            })
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    # ========================
    # User Routes
    # ========================
    
    @app.route('/users', methods=['GET'])
    def get_all_users():
        users = User.query.all()
        return jsonify([{
            'public_id': user.public_id,
            'username': user.username,
            'email': user.email,
            'name': user.name
        } for user in users])

    @app.route('/users/<public_id>', methods=['GET'])
    def get_one_user(public_id):
        user = User.query.filter_by(public_id=public_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'public_id': user.public_id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'posts_count': len(user.posts)
        })

    # ========================
    # Post Routes (Updated)
    # ========================
    
    @app.route('/posts', methods=['GET'])
    def get_posts():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return jsonify([{
            'id': p.id,
            'content': p.content,
            'author': {
                'username': p.author.username,
                'id': p.author.id
            },
            'created_at': p.created_at.isoformat()
        } for p in posts])

    @app.route('/posts', methods=['POST'])
    def add_post():
        data = request.get_json()
        user = User.query.get(data['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        post = Post(content=data['content'], author=user)
        db.session.add(post)
        db.session.commit()
        
        return jsonify({'id': post.id}), 201

    # ========================
    # Root Route
    # ========================
    
    @app.route('/')
    def home():
        return app.send_static_file('index.html')

    # Helper function for token verification
    def verify_token(token):
        if not token:
            return None
            
        try:
            # Extract token from "Bearer <token>"
            token = token.split(' ')[1]
            public_id = User.decode_token(token)  # Implement this in User model
            return User.query.filter_by(public_id=public_id).first()
        except:
            return None