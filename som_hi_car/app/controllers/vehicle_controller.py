from flask import render_template, request, redirect, url_for, jsonify
from app.models import Vehicle, TipusVehicle
from database.db import db

class VehicleController:
    @staticmethod
    def create_vehicle():
        if request.method == 'POST':
            try:
                data = request.form
                nou_vehicle = Vehicle(
                    matricula=data['matricula'],
                    marca=data['marca'],
                    model=data['model'],
                    color=data['color'],
                    num_places=int(data['num_places']),
                    tipus_vehicle_id=int(data['tipus_vehicle_id'])
                )
                db.session.add(nou_vehicle)
                db.session.commit()
                return redirect(url_for('main.vehicles'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        tipus_vehicles = TipusVehicle.query.all()
        return render_template('vehicles/nou.html', tipus_vehicles=tipus_vehicles)

    @staticmethod
    def get_vehicles():
        vehicles = Vehicle.query.all()
        return render_template('vehicles/index.html', vehicles=vehicles)

    @staticmethod
    def edit_vehicle(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404

        if request.method == 'POST':
            try:
                data = request.form
                vehicle.matricula = data['matricula']
                vehicle.marca = data['marca']
                vehicle.model = data['model']
                vehicle.color = data['color']
                vehicle.num_places = int(data['num_places'])
                vehicle.tipus_vehicle_id = int(data['tipus_vehicle_id'])
                db.session.commit()
                return redirect(url_for('main.vehicles'))
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        tipus_vehicles = TipusVehicle.query.all()
        return render_template('vehicles/editar.html', vehicle=vehicle, tipus_vehicles=tipus_vehicles)

    @staticmethod
    def delete_vehicle(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        try:
            db.session.delete(vehicle)
            db.session.commit()
            return redirect(url_for('main.vehicles'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400