from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_socketio import SocketIO, emit
from config import Config
from dotenv import load_dotenv # Import load_dotenv
import os

# REMOVE: from .controllers.auth_controller import AuthRegister, AuthLogin, AuthLogout

load_dotenv()

# Initialize extensions outside the factory
db = SQLAlchemy()
socketio = SocketIO() # Initialize SocketIO

def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(flask_app)
    
    flask_app.config['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
    if not flask_app.config['GEMINI_API_KEY']:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    # Initialize Flask-RESTful with the app
    api = Api(flask_app)
    socketio.init_app(flask_app, cors_allowed_origins=["http://127.0.0.1:5173","http://localhost:5173"], async_mode='eventlet')

    # Import and register RESTful resources (Controllers)
<<<<<<< HEAD
=======
    # This ensures the 'app' module is fully initialized before controllers/services are loaded.
>>>>>>> d7c4e4c4d896bb2b2ef63b14688d0136cee378b6
    from .controllers.auth_controller import AuthRegister, AuthLogin, AuthLogout

    # Add resources to the API instance
    api.add_resource(AuthRegister, '/api/auth/register')
    api.add_resource(AuthLogin, '/api/auth/login')
    api.add_resource(AuthLogout, '/api/auth/logout')
    
    import app.services.quiz_socketio_service  # Import SocketIO service to register event handlers

    return flask_app