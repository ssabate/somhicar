from flask import flash, render_template, request, redirect, url_for, jsonify
from app.models import Sector
from database.db import db

class SectorController:
    @staticmethod
    def get_sectors():
        sectors = Sector.query.all()
        return render_template('sectors/index.html', sectors=sectors)

    @staticmethod
    def create_sector():
        if request.method == 'POST':
            try:
                data = request.form
                nou_sector = Sector(
                    descripcio=data['descripcio'],
                    es_port=bool(data.get('es_port', False))
                )
                db.session.add(nou_sector)
                db.session.commit()
                return redirect(url_for('main.sectors'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        return render_template('sectors/nou.html')

    @staticmethod
    def edit_sector(sector_id):
        sector = Sector.query.get(sector_id)
        if not sector:
            return jsonify({'error': 'Sector not found'}), 404

        if request.method == 'POST':
            try:
                data = request.form
                # Check how many sectors belongs to the port
                if sector.es_port and Sector.query.filter_by(es_port=True).count() == 1 and bool(data.get('es_port', False))==False:
                    flash('No pots canviar l\'últim sector que pertany al Port.', 'error')
                    return redirect(url_for('main.sectors'))
                    # return jsonify({'error': 'Cannot delete the last port sector'}), 400

                sector.descripcio = data['descripcio']
                sector.es_port = bool(data.get('es_port', False))
                db.session.commit()
                flash('Sector editat correctament!', 'success')
                return redirect(url_for('main.sectors'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        return render_template('sectors/editar.html', sector=sector)

    @staticmethod
    def delete_sector(sector_id):
        sector = Sector.query.get(sector_id)
        if not sector:
            return jsonify({'error': 'Sector not found'}), 404
        try:
            # Check how many sectors belongs to the port
            if sector.es_port and Sector.query.filter_by(es_port=True).count() == 1:
                flash('No pots borrar l\'últim sector que pertany al Port.', 'error')
                return redirect(url_for('main.sectors'))
                #return jsonify({'error': 'Cannot delete the last port sector'}), 400
            db.session.delete(sector)
            db.session.commit()
            flash('Sector borrat correctament!', 'success')
            return redirect(url_for('main.sectors'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400