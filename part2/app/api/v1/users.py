from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("users", description="User management")

user_model = api.model("User", {
    "id": fields.String(readOnly=True, description="Unique identifier"),
    "email": fields.String(required=True, description="Email address"),
    "first_name": fields.String(required=False, description="First name"),
    "last_name": fields.String(required=False, description="Last name"),
    "created_at": fields.String(readOnly=True, description="Creation timestamp"),
    "updated_at": fields.String(readOnly=True, description="Update timestamp")
})


@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """Retrieve all users (excluding passwords)"""
        users = facade.get_all("User")
        for user in users:
            user.pop("password", None)
        return users

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.json
        return facade.create("User", data), 201


@api.route("/<string:user_id>")
@api.param("user_id", "The user identifier")
class UserDetail(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Retrieve a user by ID (excluding password)"""
        user = facade.get("User", user_id)
        if user:
            user.pop("password", None)
            return user
        api.abort(404, "User not found")

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user by ID"""
        data = request.json
        updated = facade.update("User", user_id, data)
        if updated:
            updated.pop("password", None)
            return updated
        api.abort(404, "User not found")
