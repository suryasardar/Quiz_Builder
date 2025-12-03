class Config:
    SECRET_KEY = 'your_super_secret_key_change_me'
    GEMINI_API_KEY = 'AIzaSyC2uGhi4ce6YY0kqKavaxrM7W43unpIHh0'
    # Configure MySQL connection using Flask-SQLAlchemy format
    # Replace 'user', 'password', 'host', and 'db_name' with your details
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Mahesh%40123@db.pedrepccqcvbqawlljzc.supabase.co:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False