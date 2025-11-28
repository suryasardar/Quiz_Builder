from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import Config

# REMOVE: from .controllers.auth_controller import AuthRegister, AuthLogin, AuthLogout

# Initialize extensions outside the factory
db = SQLAlchemy()
api = Api()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app (STEP 1: db and api are ready)
    db.init_app(app)
    api.init_app(app) # Initializes Flask-RESTful

    # >>> FIX: Import and register RESTful resources (Controllers) HERE <<<
    # This ensures the 'app' module is fully initialized before controllers/services are loaded.
    from .controllers.auth_controller import AuthRegister, AuthLogin, AuthLogout

    # Add resources to the API instance
    api.add_resource(AuthRegister, '/api/auth/register')
    api.add_resource(AuthLogin, '/api/auth/login')
    api.add_resource(AuthLogout, '/api/auth/logout')

    return app