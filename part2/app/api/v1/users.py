from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository
from app.services.facade import HBnBFacade


user_repo = InMemoryRepository()
place_repo = InMemoryRepository()
review_repo = InMemoryRepository()
amenity_repo = InMemoryRepository()

api = Namespace('users', description='User operations')
facade = HBnBFacade(user_repo, place_repo, review_repo, amenity_repo)


# Modèle pour validation des entrées et documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'Users list retrieved successfully')
    def get(self):
        """Retrieve list of all users"""
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Email already registered')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Vérifier unicité email si changement d'email
        if user.email != user_data['email']:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

        updated_user = facade.update(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

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
