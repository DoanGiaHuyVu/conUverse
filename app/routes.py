from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Post

main = Blueprint('main', __name__)

@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password'],
        name=data.get('name', '')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created', 'user_id': new_user.id}), 201

@main.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(
        user_id=data['user_id'],
        content=data['content'],
        image_url=data.get('image_url')
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created', 'post_id': new_post.id}), 201