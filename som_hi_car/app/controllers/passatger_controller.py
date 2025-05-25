from flask import render_template, request, redirect, url_for, jsonify
from app.models import Passatger, Usuari
from database.db import db

class PassatgerController:
    @staticmethod
    def create_passatger():
        if request.method == 'POST':
            try:
                data = request.form
                nou_passatger = Passatger(
                    usuari_id=int(data['usuari_id']),
                    vegades_impuntuals=int(data['vegades_impuntuals']),
                    vegades_no_presentat=int(data['vegades_no_presentat']),
                    necessita_seient_davanter=bool(data.get('necessita_seient_davanter', False))
                )
                db.session.add(nou_passatger)
                db.session.commit()
                return redirect(url_for('main.passatgers'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        usuaris = Usuari.query.all()
        return render_template('passatgers/nou.html', usuaris=usuaris)

    @staticmethod
    def get_passatgers():
        passatgers = Passatger.query.all()
        return render_template('passatgers/index.html', passatgers=passatgers)

    @staticmethod
    def edit_passatger(passatger_id):
        passatger = Passatger.query.get(passatger_id)
        if not passatger:
            return jsonify({'error': 'Passatger not found'}), 404

        if request.method == 'POST':
            try:
                data = request.form
                passatger.vegades_impuntuals = int(data['vegades_impuntuals'])
                passatger.vegades_no_presentat = int(data['vegades_no_presentat'])
                passatger.necessita_seient_davanter = bool(data.get('necessita_seient_davanter', False))
                db.session.commit()
                return redirect(url_for('main.passatgers'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        return render_template('passatgers/editar.html', passatger=passatger)

    @staticmethod
    def delete_passatger(passatger_id):
        passatger = Passatger.query.get(passatger_id)
        if not passatger:
            return jsonify({'error': 'Passatger not found'}), 404
        try:
            db.session.delete(passatger)
            db.session.commit()
            return redirect(url_for('main.passatgers'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400