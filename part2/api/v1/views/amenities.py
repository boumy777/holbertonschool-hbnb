# api/v1/views/amenities.py

from flask import request
from flask_restx import Namespace, Resource, fields
from business.facade import facade

api = Namespace('amenities', description='Amenity operations')

# Modèle pour afficher/mettre à jour une amenity
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True)
})


@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Get all amenities"""
        return facade.get_all_amenities()

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.json
        amenity = facade.create_amenity(data)
        return amenity, 201


@api.route('/<amenity_id>')
@api.param('amenity_id', 'The Amenity ID')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get a single amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an existing amenity"""
        data = request.json
        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

