from flask import Blueprint, jsonify
from models import User

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{"id": user.id, "username": user.username, "role": user.role} for user in users]
    return jsonify(result), 200
