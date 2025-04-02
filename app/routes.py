from flask import Blueprint, request, jsonify
from app import mysql
import MySQLdb

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Social Media Backend API"

# User routes
@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash, name) VALUES (%s, %s, %s, %s)",
            (data['username'], data['email'], data['password'], data.get('name', ''))
        )
        mysql.connection.commit()
        user_id = cur.lastrowid
        cur.close()
        return jsonify({'message': 'User created', 'user_id': user_id}), 201
    except MySQLdb.IntegrityError as e:
        return jsonify({'error': 'Username or email already exists'}), 400

@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# Post routes
@main.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO posts (user_id, content, image_url) VALUES (%s, %s, %s)",
            (data['user_id'], data['content'], data.get('image_url', None))
        )
        mysql.connection.commit()
        post_id = cur.lastrowid
        cur.close()
        return jsonify({'message': 'Post created', 'post_id': post_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cur.fetchone()
    cur.close()
    if post:
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404

@main.route('/posts/user/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    posts = cur.fetchall()
    cur.close()
    return jsonify(posts)

# Follow routes
@main.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO followers (follower_id, followed_id) VALUES (%s, %s)",
            (data['follower_id'], data['followed_id'])
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Followed successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Like routes
@main.route('/like', methods=['POST'])
def like_post():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO likes (user_id, post_id) VALUES (%s, %s)",
            (data['user_id'], data['post_id'])
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Post liked'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400