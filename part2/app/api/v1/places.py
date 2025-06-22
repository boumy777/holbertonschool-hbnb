import uuid
from flask import request
from flask_restx import Resource, Namespace, fields

api = Namespace('places', description='Places related operations')

# In-memory storage for places
places = []
# This is a simple in-memory storage for demonstration purposes.
# In a real application, you would use a database or persistent storage.
place_model = api.model('Place',
                        {
                            'id': fields.String(readOnly=True, description='The unique identifier of the place'),
                            'title': fields.String(required=True, description='The title of the place'),
                            'description': fields.String(required=True, description='A description of the place'),
                            'price': fields.Float(required=True, description='The price of the place'),
                            'latitude': fields.Float(required=True, description='The latitude of the place'),
                            'longitude': fields.Float(required=True, description='The longitude of the place'),
                            'owner_id': fields.String(required=True, description='The owner ID of the place'),
                        })


# PlaceList Resource handles the collection of places.
# It supports GET to retrieve all places and POST to create a new place.
@api.route('/')
class PlaceList(Resource):
    # Resource for handling a collection of places
    @api.marshal_list_with(place_model)
    def get(self):
        return places, 200

    # Create a new place
    @api.expect(place_model) # Expect a JSON payload that matches the place_model
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input')
    def post(self):
        # Check if the request is JSON
        if not request.is_json:
            return {'message': 'Request must be JSON'}, 400
        data_received = request.get_json()

        # Check if the required fields are present in the request data
        required_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']

        # Ensure all required fields are present
        for verified_field in required_fields:
            if verified_field not in data_received:
                return {'message': '{} is required'.format(verified_field)}, 400
            
        # Create a new place with a unique ID
        new_place = {
            'id': str(uuid.uuid4()),
            'title': data_received.get('title'),
            'description': data_received.get('description'),
            'price': data_received.get('price'),
            'latitude': data_received.get('latitude'),
            'longitude': data_received.get('longitude'),
            'owner_id': data_received.get('owner_id'),
        }
        places.append(new_place) # Add the new place to the in-memory storage

        # Validate the input data
        if not new_place['title'] or not new_place['description'] or not isinstance(new_place['price'], (float, int)) or \
           not isinstance(new_place['latitude'], float) or not isinstance(new_place['longitude'], float):
            return {'message': 'Invalid input data'}, 400
        return new_place, 201

# PlaceResource handles operations on a single place identified by place_id.
# It supports GET to retrieve a place, PUT to update a place, and DELETE to remove a place.
@api.route('/<place_id>')
class PlaceResource(Resource):
    # Resource for handling a single place identified by place_id
    @api.marshal_with(place_model)
    @api.response(200, 'Place found')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        for place in places:
            if place['id'] == place_id:
                return place, 200
        return {'message': "Place with id {} not found".format(place_id)}, 404

    # Update a place identified by place_id
    @api.route('places/<place_id>')
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input')
    def put(self, place_id):
        if not request.is_json:
            return {'message': 'Request must be JSON'}, 400
        data_received = request.get_json()
        # Check if the required fields are present
        for place in places:
            if place['id'] == place_id:
                place['title'] = data_received.get('title', place['title'])
                place['description'] = data_received.get('description', place['description'])
                place['price'] = data_received.get('price', place['price'])
                place['latitude'] = data_received.get('latitude', place['latitude'])
                place['longitude'] = data_received.get('longitude', place['longitude'])
                place['owner_id'] = data_received.get('owner_id', place['owner_id'])
                return place, 200
        return {'message': "Place with id {} not found".format(place_id)}, 404

    # Delete a place identified by place_id
    @api.route('places/<place_id>')
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        for idx, place in enumerate(places): # Using enumerate to get index and place
            if place['id'] == place_id:
                del places[idx]
                return {'message': 'Place with id {} deleted successfully'.format(place_id)}, 200
        return {'message': "Place with id {} not found".format(place_id)}, 404