from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("amenities", description="Operations related to amenities")

# Définir le modèle pour Swagger (documentation interactive)
amenity_model = api.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True, description="Name of the amenity"),
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

@api.route("/")
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        return facade.get_all("Amenity")

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.get_json()
        return facade.create("Amenity", data), 201


@api.route("/<string:amenity_id>")
@api.param("amenity_id", "The Amenity identifier")
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get a single amenity"""
        return facade.get("Amenity", amenity_id)

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        data = request.get_json()
        return facade.update("Amenity", amenity_id, data)

    def delete(self, amenity_id):
        """Delete an amenity"""
        return facade.delete("Amenity", amenity_id), 204
