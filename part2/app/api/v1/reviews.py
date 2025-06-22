from flask_restx import Resource, Namespace, fields
from app.services.facade import HBNBFacade

api = Namespace('reviews', description='Reviews related operations')

# Define the model for a review
# api expects a JSON payload with the following fields:
review_model = api.model('Review',
                        {
                            'text': fields.String(required=True, description='The text of the review'),
                            'rating': fields.Integer(required=True, description='The rating given in the review'),
                            'place_id': fields.String(required=True, description='The ID of the place being reviewed'),
                            'user_id': fields.String(required=True, description='The ID of the user who wrote the review'),
                        })

# Define the ReviewList resource to handle review creation and retrieval
# This resource allows creating a new review or retrieving all reviews
# try/except blocks are used to handle errors gracefully
@api.route('/')
class ReviewList(Resource):
    # Create a new review via the Facade service or retrieve all reviews
    @api.expect(review_model)
    @api.response(200, 'Review successfully created')
    @api.response(404, 'Invalid input data')
    def post(self):
        try:
            review_data = api.payload # Data recovered from the request payload
            new_review = HBNBFacade().create_review(review_data)
            return new_review, 200
        except ValueError as e:
            api.abort(404, str(e))

    # Retrieve all reviews
    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'No reviews found')
    @api.response(500, 'Internal server error')
    def get(self):
        try:
            reviews = HBNBFacade().get_all_reviews()
            if reviews:
                return reviews, 200
            api.abort(404, 'No reviews found')
        except Exception as e:
            api.abort(500, 'Internal server error: {}'.format(str(e)))

# Define the ReviewResource to handle operations on a specific review by ID
# This resource allows retrieval, update, and deletion of a review
@api.route('/<review_id>')
class ReviewResource(Resource):
    # Retrieve, update, or delete a specific review by ID
    # Retrieve a review by ID
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.response(500, 'Internal server error')
    def get(self, review_id):
        try:
            review_dict = HBNBFacade().get_review(review_id)
            if not review_dict:
                api.abort(404, 'Review not found')
            return review_dict, 200
        except Exception as e:
            api.abort(500, 'Internal server error: {}'.format(str(e)))

    # Update a review by ID
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        review_data = api.payload
        try:
            update_review = HBNBFacade().update_review(review_id, review_data)
            if not update_review:
                api.abort(404, 'Review not found')
            return update_review, 200
        except ValueError as e:
            api.abort(400, str(e))

    # Delete a review by ID
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        try:
            deleted_review = HBNBFacade().delete_review(review_id)
            if not deleted_review:
                api.abort(404, 'Review not found')
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            api.abort(500, 'Internal server error: {}'.format(str(e)))

# Define the PlaceReviewList resource to handle reviews for a specific place
# This resource allows retrieval of all reviews for a specific place by place_id
@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    # Retrieve all reviews for a specific place
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        try:
            reviews = HBNBFacade().get_reviews_by_place(place_id)
            if not reviews:
                api.abort(404, 'No reviews found for this place')
            return reviews, 200
        except ValueError as e:
            api.abort(404, str(e))