from flask import render_template, request, redirect, url_for, jsonify
from app.models import Parada, Ubicacio
from database.db import db

class ParadaController:
    @staticmethod
    def get_parades():
        parades = Parada.query.order_by(Parada.separacio_port, Parada.descripcio).all()
        return render_template('parades/index.html', parades=parades)

    @staticmethod
    def create_parada():
        if request.method == 'POST':
            try:
                data = request.form
                nova_parada = Parada(
                    descripcio=data['descripcio'],
                    ubicacio_id=int(data['ubicacio_id']),
                    separacio_port=int(data['separacio_port'])
                )
                db.session.add(nova_parada)
                db.session.commit()
                return redirect(url_for('main.parades'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        ubicacions = Ubicacio.query.all()
        return render_template('parades/nou.html', ubicacions=ubicacions)

    @staticmethod
    def edit_parada(parada_id):
        parada = Parada.query.get(parada_id)
        if not parada:
            return jsonify({'error': 'Parada not found'}), 404

        if request.method == 'POST':
            try:
                data = request.form
                parada.descripcio = data['descripcio']
                parada.ubicacio_id = int(data['ubicacio_id'])
                parada.separacio_port = int(data['separacio_port'])
                db.session.commit()
                return redirect(url_for('main.parades'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        ubicacions = Ubicacio.query.all()
        return render_template('parades/editar.html', parada=parada, ubicacions=ubicacions)

    @staticmethod
    def delete_parada(parada_id):
        parada = Parada.query.get(parada_id)
        if not parada:
            return jsonify({'error': 'Parada not found'}), 404
        try:
            db.session.delete(parada)
            db.session.commit()
            return redirect(url_for('main.parades'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400