from .main import bp_main
from .auth import bp_auth

def register_blueprints(app):
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_auth)