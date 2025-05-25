from flask import render_template, request, redirect, url_for, jsonify
from app.models import TipusVehicle
from database.db import db

class TipusVehicleController:
    @staticmethod
    def get_tipus_vehicles():
        tipus_vehicles = TipusVehicle.query.all()
        return render_template('tipus_vehicles/index.html', tipus_vehicles=tipus_vehicles)

    @staticmethod
    def create_tipus_vehicle():
        if request.method == 'POST':
            try:
                data = request.form
                nou_tipus = TipusVehicle(nom=data['nom'])
                db.session.add(nou_tipus)
                db.session.commit()
                return redirect(url_for('main.tipus_vehicles'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        return render_template('tipus_vehicles/nou.html')

    @staticmethod
    def edit_tipus_vehicle(tipus_vehicle_id):
        tipus_vehicle = TipusVehicle.query.get(tipus_vehicle_id)
        if not tipus_vehicle:
            return jsonify({'error': 'TipusVehicle not found'}), 404

        if request.method == 'POST':
            try:
                data = request.form
                tipus_vehicle.nom = data['nom']
                db.session.commit()
                return redirect(url_for('main.tipus_vehicles'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        return render_template('tipus_vehicles/editar.html', tipus_vehicle=tipus_vehicle)

    @staticmethod
    def delete_tipus_vehicle(tipus_vehicle_id):
        tipus_vehicle = TipusVehicle.query.get(tipus_vehicle_id)
        if not tipus_vehicle:
            return jsonify({'error': 'TipusVehicle not found'}), 404
        try:
            db.session.delete(tipus_vehicle)
            db.session.commit()
            return redirect(url_for('main.tipus_vehicles'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400