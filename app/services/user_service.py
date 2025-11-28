from app import db
from app.models.user_model import User
from sqlalchemy.exc import IntegrityError

class UserService:
    
    @staticmethod
    def register_user(username, email, password):
        """Creates a new user and saves to the database."""
        if User.query.filter_by(username=username).first() or \
           User.query.filter_by(email=email).first():
            return None, "Username or email already exists."

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user, "User registered successfully."
        except IntegrityError:
            db.session.rollback()
            return None, "Database error during registration."

    @staticmethod
    def authenticate_user(username, password):
        """Authenticates a user by username and password."""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None