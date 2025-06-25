# app/api/v1/places.py

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("places", description="Places operations")

place_model = api.model("Place", {
    "id": fields.String(required=True),
    "name": fields.String(required=True),
    "description": fields.String,
})

@api.route("/")
class PlaceList(Resource):
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
