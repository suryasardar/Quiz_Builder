"""run.py - Application entrypoint.

Use this file to start the Flask + Socket.IO app. The previous
`app.py` filename shadowed the `app` package which caused import
conflicts. Running `python run.py` avoids that collision.
"""

from app import create_app, db, socketio

# Create the Flask application
flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        # import your models here so db.create_all() detects them
        try:
            from app import models  # adjust to your models module
        except ImportError:
            pass
        db.create_all()

    print("Starting SocketIO server on http://127.0.0.1:5000")
    # disable use_reloader to avoid double-start when debug=True
    socketio.run(flask_app, debug=True, host='127.0.0.1', port=5000, use_reloader=False)

