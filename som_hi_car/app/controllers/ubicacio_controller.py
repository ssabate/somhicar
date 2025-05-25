from flask import render_template, request, redirect, url_for, jsonify
from app.models import Ubicacio, Sector
from database.db import db

class UbicacioController:
    @staticmethod
    def get_ubicacions():
        ubicacions = Ubicacio.query.all()
        return render_template('ubicacions/index.html', ubicacions=ubicacions)

    @staticmethod
    def create_ubicacio():
        if request.method == 'POST':
            try:
                data = request.form
                nova_ubicacio = Ubicacio(
                    nom=data['nom'],
                    sector_id=int(data['sector_id'])
                )
                db.session.add(nova_ubicacio)
                db.session.commit()
                return redirect(url_for('main.ubicacions'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        sectors = Sector.query.all()
        return render_template('ubicacions/nou.html', sectors=sectors)

    @staticmethod
    def edit_ubicacio(ubicacio_id):
        ubicacio = Ubicacio.query.get(ubicacio_id)
        if not ubicacio:
            return jsonify({'error': 'Ubicació not found'}), 404

        if request.method == 'POST':
            try:
                data = request.form
                ubicacio.nom = data['nom']
                ubicacio.sector_id = int(data['sector_id'])
                db.session.commit()
                return redirect(url_for('main.ubicacions'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        sectors = Sector.query.all()
        return render_template('ubicacions/editar.html', ubicacio=ubicacio, sectors=sectors)

    @staticmethod
    def delete_ubicacio(ubicacio_id):
        ubicacio = Ubicacio.query.get(ubicacio_id)
        if not ubicacio:
            return jsonify({'error': 'Ubicació not found'}), 404
        try:
            db.session.delete(ubicacio)
            db.session.commit()
            return redirect(url_for('main.ubicacions'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400