# api/v1/views/users.py

from flask import request
from flask_restx import Namespace, Resource, fields
from business.facade import facade

api = Namespace('users', description='User operations')

# Modèle pour afficher un utilisateur (sans le mot de passe)
user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'email': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String
})

# Modèle utilisé pour la création (inclut le password)
user_create_model = api.model('UserCreate', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String
})


@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        return facade.get_all_users()

    @api.expect(user_create_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.json
        user = facade.create_user(data)
        return user, 201


@api.route('/<user_id>')
@api.param('user_id', 'The user ID')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a single user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update an existing user"""
        data = request.json
        user = facade.update_user(user_id, data)
        if not user:
            api.abort(404, "User not found")
        return user

