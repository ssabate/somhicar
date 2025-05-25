from flask import Blueprint

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    from app.controllers.auth.auth_controller import AuthController
    return AuthController.register()

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    from app.controllers.auth.auth_controller import AuthController
    return AuthController.login()

@bp_auth.route('/logout')
def logout():
    from app.controllers.auth.auth_controller import AuthController
    return AuthController.logout()