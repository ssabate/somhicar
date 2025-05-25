from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))  # Redirigir al login si no está autenticado
        if not current_user.super_admin:
            abort(403)  # Denegar acceso si no es super_admin
        return f(*args, **kwargs)
    return decorated_function

def conductor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.conductor:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def admin_or_conductor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not (current_user.super_admin or current_user.conductor):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function