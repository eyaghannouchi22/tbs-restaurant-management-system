from flask import Blueprint, request, jsonify
from models import Meal, User
from sqlalchemy.exc import SQLAlchemyError
from database import db


meal_routes = Blueprint('meal_routes', __name__)

@meal_routes.route('/meals', methods=['GET', 'POST', 'PUT'])
def meals():
    if request.method == 'GET':
        meals = Meal.query.all()
        result = [{"id": meal.id, "name": meal.name, "available": meal.available} for meal in meals]
        return jsonify(result), 200

    data = request.get_json()

    if request.method == 'POST':
        staff_id = data.get('staff_id')
        staff_member = User.query.get(staff_id)
        if not staff_member or staff_member.role != 'staff':
            return jsonify({"error": "Unauthorized access. Only staff can add meals."}), 403

        if not data.get('name'):
            return jsonify({"error": "Meal name is required."}), 400

        new_meal = Meal(name=data['name'], available=data.get('available', True))
        db.session.add(new_meal)
        db.session.commit()
        return jsonify({"message": "Meal added successfully!", "meal_id": new_meal.id}), 201

    if request.method == 'PUT':
        if 'meal_id' not in data:
            return jsonify({"error": "meal_id is required"}), 400

        meal = Meal.query.get(data['meal_id'])

        if not meal:
            return jsonify({"error": "Meal not found"}), 404

        meal.name = data.get('name', meal.name)
        meal.available = data.get('available', meal.available)
        db.session.commit()
        return jsonify({"message": "Meal updated successfully!"}), 200
