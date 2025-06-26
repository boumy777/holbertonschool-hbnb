from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from app.persistence.repository import user_repo, place_repo, review_repo, amenity_repo


facade = HBnBFacade(user_repo, place_repo, review_repo, amenity_repo)
api = Namespace('places', description='Place operations')


amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

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

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'address': fields.String(required=True, description='Address of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):


    def get(self):
        places = facade.get_all("Place")
        return [p.to_dict() for p in places]

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')


    def post(self):
        """Register a new place"""
        place_data = api.payload

        owner_id = place_data['owner_id']
        print(f"ID de l'utilisateur à récupérer : {owner_id}")
        owner = facade.get_user(owner_id)

        if not owner:
            return {'error': 'Owner not found'}, 404

        new_place = facade.create_place(place_data)

        return {
            'title': new_place.title,
            'id': new_place.id,
            'description': new_place.description,
            'price': new_place.price,
            'address': new_place.address,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'amenities': new_place.amenities,
            "owner_id": new_place.owner.id
        }, 201
    
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        places_data = []
        for place in places:
            places_data.append({
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "address": place.address,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner": {
                    "id": place.owner.id,
                    "first_name": place.owner.first_name,
                    "last_name": place.owner.last_name
                },
                "amenities": place.amenities,
                "reviews": [{"id": r.id, "text": r.text, "rating": r.rating, "user_id": r.user.id} for r in place.reviews]
            })
        return places_data, 200


@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)

        if place is None:
            return {"error": "Place not found"}, 404

        return {
            'id': place['id'],
            'title': place['title'],
            'description': place['description'],
            'price': place['price'],
            'address': place['address'],
            'latitude': place['latitude'],
            'longitude': place['longitude'],
            'owner_id': place['owner']['id'],
            'amenities': place['amenities'],
            'reviews': place['reviews']
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload

        place = facade.update_place(place_id, data)

        if place is None:
            return {"error": "Place not found"}, 404

        place_data = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'address': place.address,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name
            },
            'amenities': place.amenities
        }

        return place_data, 200

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
