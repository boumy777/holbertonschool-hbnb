# app/api/v1/places.py

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("places", description="Places operations")

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route("/")
class PlaceList(Resource):
    api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def get(self):
        places = facade.get_all("Place")
        return [p.to_dict() for p in places]

    def post(self):
        data = api.payload
        new_place = facade.create("Place", data)
        return new_place.to_dict(), 201


@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_by_id("Place", place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict()

    def put(self, place_id):
        data = api.payload
        updated = facade.update("Place", place_id, data)
        if not updated:
            api.abort(404, "Place not found")
        return updated.to_dict()

    def delete(self, place_id):
        success = facade.delete("Place", place_id)
        if not success:
            api.abort(404, "Place not found")
        return {"message": "Deleted successfully"}
