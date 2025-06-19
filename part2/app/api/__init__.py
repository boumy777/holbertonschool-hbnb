# api/__init__.py

from flask import Flask
from flask_restx import Api

from api.v1.views.users import api as users_ns
from api.v1.views.amenities import api as amenities_ns

def create_app():
    """Factory Flask App"""
    app = Flask(__name__)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API for managing users, places, reviews, and amenities in HBnB project',
        doc='/swagger'  # Swagger UI at /swagger
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app
