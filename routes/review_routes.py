from flask import Blueprint, request, jsonify
from models import Review, User, Meal
from sqlalchemy.exc import SQLAlchemyError

review_routes = Blueprint('review_routes', __name__)

@review_routes.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = Review.query.all()
        review_list = [
            {"id": review.id, "user_id": review.user_id, "meal_id": review.meal_id, "comment": review.comment, "rating": review.rating}
            for review in reviews
        ]
        return jsonify(review_list), 200

    if request.method == 'POST':
        data = request.get_json()

        if not data.get('user_id') or not data.get('meal_id') or not data.get('comment') or not data.get('rating'):
            return jsonify({"error": "Missing required fields: user_id, meal_id, comment, or rating"}), 400

        user = User.query.get(data['user_id'])
        meal = Meal.query.get(data['meal_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not meal:
            return jsonify({"error": "Meal not found"}), 404

        new_review = Review(user_id=data['user_id'], meal_id=data['meal_id'], comment=data['comment'], rating=data['rating'])
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review submitted successfully!", "review_id": new_review.id}), 201
