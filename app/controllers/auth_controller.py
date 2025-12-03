from flask import request
from flask_restful import Resource
from app.services.user_service import UserService
import re

class AuthRegister(Resource):
    def post(self):
        data = request.get_json() or {}

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not username or not email or not password:
            return {'message': 'Username, email and password required'}
        
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return {'message': 'Missing data fields.'}, 400
        
        #username validation
        if len(username) < 3 or len(username) > 20 or " " in username:
            return {'message': 'Invalid username: must be 3-20 chars and contain no spaces.'}, 400

        #email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, data['email']):
            return {'message':'Inavlid email format'},400

        user, message = UserService.register_user(
            data['username'], data['email'], data['password']
        )

        # Password validation
        password_pattern = r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z0-9@$!%*?&]{8,}$'
        if not re.match(password_pattern, password):
            return {
                'message': 'Password must contain: 8+ chars, 1 uppercase letter, 1 number, 1 special character.'
            }, 400
        user, message = UserService.register_user(username, email, password)

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
            token = f"token-{user.id}"
            return {
                'message':'Login Successful',
                'username': user.username,
                'token': token
            },200
        
        return {'message': 'Invalid credentials'}, 401

blacklist = set()
class AuthLogout(Resource):
    def post(self):
        token_header = request.headers.get("Authorization")
        
        if not token_header:
            return {'message': 'Auth token missing.'}, 400
        
        token = token_header.replace("Bearer ", "")
        blacklist.add(token)

        return {'message': 'Logged out successfully. Token blacklisted.'}, 200