from flask import Blueprint, request, jsonify
from models import User, Meal, Reservation
from sqlalchemy.exc import SQLAlchemyError

reservation_routes = Blueprint('reservation_routes', __name__)

@reservation_routes.route('/reservations', methods=['GET', 'POST'])
def handle_reservations():
    if request.method == 'GET':
        reservations = Reservation.query.all()
        result = [{"id": res.id, "user_id": res.user_id, "meal_id": res.meal_id} for res in reservations]
        return jsonify(result), 200

    elif request.method == 'POST':
        data = request.get_json()
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        meal = Meal.query.get(data['meal_id'])
        if not meal:
            return jsonify({"error": "Meal not found"}), 404
        if not meal.available:
            return jsonify({"error": "Meal is no longer available for reservation"}), 400
        existing_reservation = Reservation.query.filter_by(user_id=data['user_id'], meal_id=data['meal_id']).first()
        if existing_reservation:
            return jsonify({"error": "You have already reserved this meal"}), 400
        reservation = Reservation(user_id=data['user_id'], meal_id=data['meal_id'])
        db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Meal reserved successfully!"}), 201
