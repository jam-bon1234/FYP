from flask import Blueprint

from flask import Blueprint

preferences_bp = Blueprint('preferences', __name__)
auth_bp = Blueprint('auth', __name__)
user_bp = Blueprint('user', __name__)
maps_bp = Blueprint("maps", __name__)

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(preferences_bp, url_prefix="/preferences")
    app.register_blueprint(maps_bp, url_prefix="/maps")