from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from sqlalchemy.exc import SQLAlchemyError
from app import db  # Ensure you import db from your app

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({"error": "Missing required fields: username, password, or role"}), 400

    if not data['password'].strip():
        return jsonify({"error": "Password cannot be empty"}), 400

    valid_roles = ['user', 'admin']
    if data['role'] not in valid_roles:
        return jsonify({"error": "Invalid role provided"}), 400

    try:
        # Hash the password and create the new user
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], password=hashed_password, role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    try:
        # Find the user by username
        user = User.query.filter_by(username=data['username']).first()

        # Check password
        if user and check_password_hash(user.password, data['password']):
            return jsonify({"message": f"Welcome {user.username}!"}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
