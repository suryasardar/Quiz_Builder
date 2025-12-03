from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY # Import for PostgreSQL array type
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """Hashes the password and sets it to the model instance."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    quizzes = db.relationship('Quiz', backref='creator', lazy='dynamic')
    attempts = db.relationship('Attempt', backref='user_attempt', lazy='dynamic')
    
    
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    # Table 1: quizzes
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic = db.Column(db.Text, nullable=False)
    generated_at = db.Column(db.DateTime(timezone=True), default=func.now)
    is_public = db.Column(db.Boolean, default=False)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic')
    attempts = db.relationship('Attempt', backref='quiz_attempt', lazy='dynamic')

    def __repr__(self):
        return f'<Quiz {self.topic} by User {self.user_id}>'


class Question(db.Model):
    __tablename__ = 'questions'
    
    # Table 2: questions
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    
    # Use PostgreSQL ARRAY type to store options as an array of strings
    options = db.Column(ARRAY(db.Text), nullable=False)
    
    # The 0-based index of the correct answer (e.g., 0, 1, 2, or 3)
    correct_index = db.Column(db.SmallInteger, nullable=False) 

    def __repr__(self):
        return f'<Question {self.id} on Quiz {self.quiz_id}>'


class Attempt(db.Model):
    __tablename__ = 'attempts'
    
    # Table 3: attempts
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Scores
    score_correct = db.Column(db.Integer, nullable=False)
    score_total = db.Column(db.Integer, nullable=False, default=20) # Default for 20 MCQs
    marks_obtained = db.Column(db.Numeric(4, 2), nullable=True) # Score out of 10
    
    # Timestamps
    started_at = db.Column(db.DateTime(timezone=True), default=func.now)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f'<Attempt {self.id} by User {self.user_id} Score {self.score_correct}/{self.score_total}>'
 