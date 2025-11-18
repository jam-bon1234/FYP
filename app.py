from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from Routes.auth import auth_bp
from Routes.user import user_bp
from Routes.preferences import preferences_bp
import os

load_dotenv()
# Code for creating database connections from tutorials slightly altered to allow for cross-origin resource sharing
app = Flask(__name__)
CORS(app)


app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(preferences_bp)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)