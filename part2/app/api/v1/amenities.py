from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.persistence.repository import user_repo, place_repo, review_repo, amenity_repo


api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade(user_repo, place_repo, review_repo, amenity_repo)

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload
        try:
            amenity = facade.create_amenity(data)
            return {'id': amenity.id, 'name': amenity.name}, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return {'id': amenity.id, 'name': amenity.name}, 200
        except LookupError:
            api.abort(404, 'Amenity not found')

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        try:
            amenity = facade.update_amenity(amenity_id, data)
            return {'message': 'Amenity updated successfully'}, 200
        except LookupError:
            api.abort(404, 'Amenity not found')
        except ValueError as e:
            api.abort(400, str(e))
