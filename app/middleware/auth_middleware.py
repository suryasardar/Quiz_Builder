from functools import wraps
from flask import session, jsonify

def login_required_api(f):
    """A decorator to check if the user is logged in (via session)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            # Return an error message suitable for an API
            return jsonify({'message': 'Authorization required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Example of a new protected controller (not included in the setup above):
# class UserProfile(Resource):
#     @login_required_api
#     def get(self):
#         return {'user_id': session.get('user_id'), 
#                 'username': session.get('username')}, 200