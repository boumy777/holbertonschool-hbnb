# app/api/v1/reviews.py

from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace("reviews", description="Operations related to reviews")

review_model = api.model("Review", {
    "user_id": fields.String(required=True, description="ID of the user"),
    "place_id": fields.String(required=True, description="ID of the place"),
    "text": fields.String(required=True, description="Review text"),
    "rating": fields.Integer(required=True, description="Rating from 1 to 5"),
})

@api.route("/")
class ReviewResource(Resource):
    @api.expect(review_model)
    def post(self):
        review_data = request.get_json()

        # ✅ Vérification du champ rating
        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Le rating doit être un entier entre 1 et 5"}, 400

        try:
            new_review = facade.create_review(review_data)
            return new_review, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def get(self):
        try:
            reviews = facade.get_all("Review")
            return reviews, 200
        except Exception as e:
            return {"error": str(e)}, 500
