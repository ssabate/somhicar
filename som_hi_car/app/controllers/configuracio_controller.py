from flask import render_template, request, redirect, url_for, flash

from app.daos.configuracio_dao import ConfiguracioDAO
from app.models import Configuracio
from database.db import db

class ConfiguracioController:

    @staticmethod
    def editar_configuracio():
        config_dao = ConfiguracioDAO(db)
        config = config_dao.get_by_id(1)
        if request.method == 'POST':
            try:
                config.pagament_activat = bool(request.form.get('pagament_activat', False))
                # Añade aquí otros parámetros si los tienes
                db.session.commit()
                flash('Configuració actualitzada correctament!', 'success')
                return redirect(url_for('main.config'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}', 'error')
        return render_template('configuracio/editar.html', config=config)