from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("users", description="User operations")

# 🔹 Schéma d'entrée (POST)
user_input = api.model("UserInput", {
    "first_name": fields.String(required=True, description="First name"),
    "last_name": fields.String(required=True, description="Last name"),
    "email": fields.String(required=True, description="Email address")
})

# 🔸 Schéma de sortie (GET, réponse POST)
user_output = api.inherit("UserOutput", user_input, {
    "id": fields.String(readOnly=True, description="User ID"),
    "created_at": fields.String(readOnly=True, description="Creation time"),
    "updated_at": fields.String(readOnly=True, description="Last update time")
})

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_output)
    def get(self):
        """Get all users (excluding password)"""
        users = facade.get_all("User")
        for user in users:
            user.pop("password", None)
        return users

    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output, code=201)
    def post(self):
        """Create a new user"""
        data = request.json

        # Vérifie que l'email est unique
        if facade.get_user_by_email(data["email"]):
            api.abort(400, "Email already registered")

        new_user = facade.create_user(data)
        return new_user, 201

@api.route("/<string:user_id>")
@api.param("user_id", "User ID")
class UserDetail(Resource):
    @api.marshal_with(user_output)
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get("User", user_id)
        if not user:
            api.abort(404, "User not found")
        user.pop("password", None)
        return user

    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output)
    def put(self, user_id):
        """Update user by ID"""
        data = request.json
        updated = facade.update("User", user_id, data)
        if not updated:
            api.abort(404, "User not found")
        updated.pop("password", None)
        return updated
