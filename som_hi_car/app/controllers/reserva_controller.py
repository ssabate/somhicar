from datetime import datetime

from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user

from app.daos.configuracio_dao import ConfiguracioDAO
from app.models import Reserva, Viatge, Passatger, Parada
from database.db import db


class ReservaController:
    @staticmethod
    def get_reserves():
        # Initialize variables
        reserves = []
        has_passatger = False

        # Check if user is authenticated and has a passatger role
        if current_user.is_authenticated and hasattr(current_user, 'passatger') and current_user.passatger:
            has_passatger = True
            reserves = Reserva.query.filter(Reserva.passatger_id == current_user.passatger.id, Reserva.viatge.has(realitzat=False)).all()

        # Fetch all available trips (viatges) with remaining seats, except the ones created by the current user, ordered by start date descending
        viatges = Viatge.query.filter(Viatge.places_restants > 0, ~Viatge.realitzat).filter(~Viatge.conductor.has(usuari_id=current_user.id)).order_by(Viatge.data_hora_inici.desc()).all()

        # Fetch configuration settings
        config_dao = ConfiguracioDAO(db)
        config = config_dao.get_by_id(1)

        return render_template('reserves/index.html', reserves=reserves, viatges=viatges, has_passatger=has_passatger, config=config)


    @staticmethod
    def get_reserves_viatge(viatge_id):
        # Initialize variables
        reserves = []

        # get the reservations of the trip
        reserves = Reserva.query.filter_by(viatge_id=viatge_id).all()

        # Fetch the trip (viatge) which reservations we're looking for
        viatge = Viatge.query.filter_by(id=viatge_id).all()

        return render_template('reserves/llista.html', reserves=reserves, viatge=viatge)

    @staticmethod
    def create_reserva(viatge_id):
        viatge = Viatge.query.get(viatge_id)
        if not viatge:
            flash('Viatge no trobat.', 'error')
            return redirect(url_for('main.reserves'))

        if request.method == 'POST':
            # Ensure the user is authenticated and has a Passatger relationship
            if not current_user.is_authenticated or not hasattr(current_user,
                                                                'passatger') or not current_user.passatger:
                flash("Has d'iniciar sessió i tenir un perfil de passatger per fer una reserva.", "warning")
                return redirect(url_for('auth.login'))

            try:
                # Create a new reservation
                nova_reserva = Reserva(
                    viatge_id=viatge_id,
                    passatger_id=current_user.passatger.id,
                    data_hora_realitzacio=datetime.utcnow(),
                    parada_recollida_id=viatge.parada_recollida_id,
                    parada_arribada_id=viatge.parada_arribada_id,
                    confirmada_passatger=True
                )
                viatge.places_restants -= 1  # Decrease available seats
                db.session.add(nova_reserva)
                db.session.commit()
                flash('Reserva creada amb èxit!', 'success')
                return redirect(url_for('main.reserves'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error en crear la reserva: {str(e)}', 'error')
                return redirect(url_for('main.reserves'))
        # Fetch configuration settings
        config_dao = ConfiguracioDAO(db)
        config = config_dao.get_by_id(1)
        return render_template('reserves/nou.html', viatge=viatge, config=config)

    @staticmethod
    def edit_reserva(reserva_id,conductor):
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            flash('Reserva no trobada.', 'error')
            return redirect(url_for('main.reserves'))

        return render_template('reserves/editar.html', reserva=reserva, conductor=conductor)



    @staticmethod
    def delete_reserva(reserva_id,conductor):
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            flash('Reserva no trobada.', 'error')
            return redirect(url_for('main.reserves'))

        try:
            # Increment the remaining places in the associated trip
            viatge = reserva.viatge
            if viatge:
                viatge.places_restants += 1

            # Delete the reservation
            db.session.delete(reserva)
            db.session.commit()
            flash('Reserva eliminada amb èxit!', 'success')
            if conductor==1:
                return redirect(url_for('main.reserves_viatge', viatge_id=viatge.id))
            else:
                return redirect(url_for('main.reserves', viatge_id=viatge.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error en eliminar la reserva: {str(e)}', 'error')
            return redirect(url_for('main.reserves'))

    @staticmethod
    def confirma_reserva(reserva_id):
        reserva = Reserva.query.get(reserva_id)

        viatge = reserva.viatge

        if not reserva:
            flash('Reserva no trobada.', 'error')
            return redirect(url_for('main.reserves_viatge', viatge_id=viatge.id))

        try:
            # The driver has confirmed the reservation
            reserva.confirmada_conductor = True

            # Save the reservation
            db.session.merge(reserva)
            db.session.commit()
            flash('Reserva confirmada amb èxit!', 'success')
            return redirect(url_for('main.reserves_viatge', viatge_id=viatge.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error en confirmar la reserva: {str(e)}', 'error')
            return redirect(url_for('main.reserves_viatge', viatge_id=viatge.id))


    @staticmethod
    def delete_reserva_viatge(reserva_id):
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            flash('Reserva no trobada.', 'error')
            return redirect(url_for('main.reserves'))

        try:
            # Increment the remaining places in the associated trip
            viatge = reserva.viatge
            if viatge:
                viatge.places_restants += 1

            # Delete the reservation
            db.session.delete(reserva)
            db.session.commit()
            flash('Reserva eliminada amb èxit!', 'success')
            return redirect(url_for('main.reserves_viatge({viatge.id})'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error en eliminar la reserva: {str(e)}', 'error')
            return redirect(url_for('main.reserves'))