from flask import render_template, request, redirect, url_for, jsonify, flash
from app.models import Conductor, Usuari
from database.db import db

class ConductorController:
    @staticmethod
    def create_conductor():
        if request.method == 'POST':
            try:
                data = request.form
                usuari_id = int(data['usuari_id'])
                # Verificar que el usuario existe
                usuari = Usuari.query.get(usuari_id)
                if not usuari:
                    flash('Usuari no trobat.', 'error')
                    return redirect(url_for('main.conductors'))
                # Verificar si el usuario ya es conductor
                if usuari.conductor:
                    flash('Aquest usuari ja és conductor.', 'error')
                    return redirect(url_for('main.conductors'))
                nou_conductor = Conductor(
                    usuari_id=usuari_id,
                    carnet_categoria_superior=data['carnet_categoria_superior'],
                    accidents_tinguts=int(data['accidents_tinguts'])
                )
                db.session.add(nou_conductor)
                db.session.commit()
                flash('Conductor creat amb èxit.', 'success')
                return redirect(url_for('main.conductors'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error en crear el conductor: {str(e)}', 'error')
                return redirect(url_for('main.conductors'))
        # Obtener usuarios que no son conductores
        usuaris = Usuari.query.filter(Usuari.conductor == None).all()
        return render_template('conductors/nou.html', usuaris=usuaris)

    @staticmethod
    def get_conductors():
        conductors = Conductor.query.all()
        return render_template('conductors/index.html', conductors=conductors)

    @staticmethod
    def edit_conductor(conductor_id):
        conductor = Conductor.query.get(conductor_id)
        if not conductor:
            flash('Conductor no trobat.', 'error')
            return redirect(url_for('main.conductors'))

        if request.method == 'POST':
            try:
                data = request.form
                conductor.carnet_categoria_superior = data['carnet_categoria_superior']
                conductor.accidents_tinguts = int(data['accidents_tinguts'])
                db.session.commit()
                flash('Conductor actualitzat amb èxit.', 'success')
                return redirect(url_for('main.conductors'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error en actualitzar el conductor: {str(e)}', 'error')
                return redirect(url_for('main.conductors'))

        return render_template('conductors/editar.html', conductor=conductor)

    @staticmethod
    def delete_conductor(conductor_id):
        conductor = Conductor.query.get(conductor_id)
        if not conductor:
            flash('Conductor no trobat.', 'error')
            return redirect(url_for('main.conductors'))
        try:
            db.session.delete(conductor)
            db.session.commit()
            flash('Conductor eliminat amb èxit.', 'success')
            return redirect(url_for('main.conductors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error en eliminar el conductor: {str(e)}', 'error')
            return redirect(url_for('main.conductors'))