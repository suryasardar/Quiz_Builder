from flask import request, session
from flask_restful import Resource
from app.services.user_service import UserService

class AuthRegister(Resource):
    def post(self):
        data = request.get_json()
        
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return {'message': 'Missing data fields.'}, 400

        user, message = UserService.register_user(
            data['username'], data['email'], data['password']
        )
        
        if user:
            return {'message': message}, 201
        return {'message': message}, 409 # Conflict

class AuthLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = UserService.authenticate_user(username, password)
        
        if user:
            # Successful login: set session variables
            session['logged_in'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            return {'message': 'Login successful', 'username': user.username}, 200
        
        return {'message': 'Invalid credentials'}, 401

class AuthLogout(Resource):
    def post(self):
        # Clear session variables
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('username', None)
        return {'message': 'Logout successful'}, 200