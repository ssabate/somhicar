from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import joinedload

from app.inicialitzar_dades import inserta_dades_base
from config import Config
from database.db import db
from app.views import register_blueprints

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    """Format a datetime object as a string."""
    return value.strftime(format)

def create_app():
    app = Flask(__name__)

    # Carregar la configuració des de config.py
    app.config.from_object(Config)
    app.logger.debug(f"db type before init_app: {type(db)}")  # Debug

    # Inicialitzar SQLAlchemy amb l'app
    db.init_app(app)
    app.logger.debug(f"db type after init_app: {type(db)}")  # Debug
    app.logger.debug(f"db.session available: {hasattr(db, 'session')}")  # Debug


    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Registrar les rutes (blueprints)
    register_blueprints(app)

    # Register Jinja2 filters
    app.jinja_env.filters['datetimeformat'] = datetimeformat

    # Importar models després de db.init_app i register_blueprints
    from app.models import Usuari, Sector

    # User loader per Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(Usuari).options(
            joinedload(Usuari.conductor),
            joinedload(Usuari.passatger),
            joinedload(Usuari.ubicacio)
        ).get(int(user_id))

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # Crear taules
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Taules inicialitzades correctament")
            inserta_dades_base()
            app.logger.info("Dades base inicialitzades correctament")
        except Exception as e:
            app.logger.error(f"Error al crear les taules: {e}")

    # Configurar el scheduler que actualiza el viatges realitzats segons la data
    with app.app_context():
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            scheduler = BackgroundScheduler()
            from app.controllers.viatge_controller import ViatgeController
            scheduler.add_job(ViatgeController.update_viatges_realitzats(),'interval', minutes=1)
            scheduler.start()
        except Exception as e:
            app.logger.error(f"Error al procés en segon pla: {e}")


    return app