from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

facade = HBnBFacade()
api = Namespace('places', description='Place operations')


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
