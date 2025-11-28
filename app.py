from app import create_app, db

# Factory function creates the app instance
app = create_app()

# Context to create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Running in debug mode for development
    app.run(debug=True)