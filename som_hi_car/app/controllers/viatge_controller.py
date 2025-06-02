from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_required
from datetime import datetime
from app.models import Viatge, Vehicle, Conductor, Parada
from database.db import db
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ViatgeController:
    @staticmethod
    @login_required
    def get_viatges(realitzat):
        logger.debug(f"Fetching trips for user ID: {current_user.id}, super_admin: {current_user.super_admin}")
        if current_user.super_admin:
            viatges = Viatge.query.all()
        else:
            viatges = Viatge.query.filter(Viatge.conductor.has(usuari_id=current_user.id)).order_by(Viatge.data_hora_inici.desc()).all()

        # Filter trips based on 'realitzat' status: 0 (all), 1 (not realized), 2 (realized)
        if realitzat!=0:
            if realitzat==1:
                viatges = [viatge for viatge in viatges if viatge.realitzat == False]
            else:
                viatges = [viatge for viatge in viatges if viatge.realitzat == True]

        parades = Parada.query.all()
        logger.debug(f"Found {len(viatges)} trips")
        return render_template('Viatges.html', viatges=viatges, parades=parades, realitzat=realitzat)



    @staticmethod
    @login_required
    def create_viatge():
        if not current_user.conductor:
            logger.warning(f"User ID: {current_user.id} attempted to create trip without conductor status")
            flash('Només els conductors poden crear viatges.', 'error')
            return redirect(url_for('main.viatges'))

        if request.method == 'POST':
            try:
                data = request.form
                conductor = Conductor.query.filter_by(usuari_id=current_user.id).first()
                nou_viatge = Viatge(
                    data_hora_inici=datetime.strptime(data['data_hora_inici'], '%Y-%m-%dT%H:%M'),
                    places_inicials=int(data['places_inicials']),
                    places_restants=int(data['places_inicials']),
                    vehicle_id=int(data['vehicle_id']),
                    conductor_id=conductor.id,
                    parada_recollida_id=int(data['parada_recollida_id']),
                    parada_arribada_id=int(data['parada_arribada_id']),
                    #sentit=data['sentit'],
                    confirmat=False,
                    realitzat=False,
                    import_=float(data['import_']),
                    observacions=data['observacions']
                )
                nou_viatge.sentit = 'Muntada' if Parada.query.filter_by(id=nou_viatge.parada_recollida_id).first().separacio_port >= Parada.query.filter_by(id=nou_viatge.parada_arribada_id).first().separacio_port else 'Baixada',

                # Verify vehicle belongs to conductor
                vehicle = Vehicle.query.get(nou_viatge.vehicle_id)
                if vehicle not in conductor.vehicles:
                    logger.error(f"Vehicle ID: {nou_viatge.vehicle_id} not owned by conductor ID: {conductor.id}")
                    flash('No pots seleccionar un vehicle que no és teu.', 'error')
                    return redirect(url_for('main.create_viatge'))

                # Mirem que un i només un sector de les parades pertanyigue al Port
                sector_inici=Parada.query.filter_by(id=nou_viatge.parada_recollida_id).first().ubicacio.sector
                sector_fi = Parada.query.filter_by(id=nou_viatge.parada_arribada_id).first().ubicacio.sector
                logger.error(f"User ID: {sector_inici} attempted to create trip without conductor status")
                if (not sector_inici.es_port and not sector_fi.es_port) or (sector_inici.es_port and sector_fi.es_port):
                    flash('Una i només una parada ha de ser del Port.', 'error')
                    return redirect(url_for('main.create_viatge'))


                db.session.add(nou_viatge)
                db.session.commit()
                logger.debug(f"Created trip ID: {nou_viatge.id} by user ID: {current_user.id}")
                flash('Viatge creat correctament!', 'success')
                return redirect(url_for('main.viatges'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error creating trip: {str(e)}")
                flash(f'Error en crear el viatge: {str(e)}', 'error')
                return redirect(url_for('main.create_viatge'))

        vehicles = Vehicle.query.join(Conductor.vehicles).filter(Conductor.usuari_id == current_user.id).all()
        parades = Parada.query.order_by(Parada.separacio_port).all()
        return render_template('viatges/nou.html', now=datetime.now, vehicles=vehicles, conductors=[current_user.conductor], parades=parades)

    @staticmethod
    @login_required
    def edit_viatge(viatge_id):
        viatge = Viatge.query.get(viatge_id)
        if not viatge:
            logger.error(f"Trip ID: {viatge_id} not found")
            flash('Viatge no trobat.', 'error')
            return redirect(url_for('main.viatges'))

        if not current_user.super_admin and viatge.conductor.usuari_id != current_user.id:
            logger.warning(f"User ID: {current_user.id} attempted to edit trip ID: {viatge_id} not owned")
            flash('No tens permís per editar aquest viatge.', 'error')
            return redirect(url_for('main.viatges'))

        if request.method == 'POST':
            try:
                data = request.form
                viatge.observacions = data['observacions']
                viatge.data_hora_inici = datetime.strptime(data['data_hora_inici'], '%Y-%m-%dT%H:%M')
                viatge.places_inicials = int(data['places_inicials'])
                viatge.places_restants = int(data['places_restants'])
                viatge.vehicle_id = int(data['vehicle_id'])
                viatge.conductor_id = int(data['conductor_id'])
                viatge.parada_recollida_id = int(data['parada_recollida_id'])
                viatge.parada_arribada_id = int(data['parada_arribada_id'])
                viatge.sentit = 'Muntada' if Parada.query.filter_by(id=viatge.parada_recollida_id).first().separacio_port >= Parada.query.filter_by(id=viatge.parada_arribada_id).first().separacio_port else 'Baixada'

                viatge.import_ = float(data['import_'])
                viatge.observacions = data['observacions']

                # Verify vehicle belongs to conductor
                vehicle = Vehicle.query.get(viatge.vehicle_id)
                conductor = Conductor.query.get(viatge.conductor_id)
                if vehicle not in conductor.vehicles:
                    logger.error(f"Vehicle ID: {viatge.vehicle_id} not owned by conductor ID: {viatge.conductor_id}")
                    flash('No pots seleccionar un vehicle que no és teu.', 'error')
                    return redirect(url_for('main.edit_viatge', viatge_id=viatge_id))

                # Mirem que un i només un sector de les parades pertanyigue al Port
                sector_inici = Parada.query.filter_by(id=viatge.parada_recollida_id).first().ubicacio.sector
                sector_fi = Parada.query.filter_by(id=viatge.parada_arribada_id).first().ubicacio.sector
                logger.error(f"User ID: {sector_inici} attempted to create trip without conductor status")
                if (not sector_inici.es_port and not sector_fi.es_port) or (
                        sector_inici.es_port and sector_fi.es_port):
                    flash('Una i només una parada ha de ser del Port.', 'error')
                    return redirect(url_for('main.edit_viatge', viatge_id=viatge_id))

                db.session.commit()
                logger.debug(f"Updated trip ID: {viatge_id} by user ID: {current_user.id}")
                flash('Viatge actualitzat correctament!', 'success')
                return redirect(url_for('main.viatges'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating trip ID: {viatge_id}: {str(e)}")
                flash(f'Error en actualitzar el viatge: {str(e)}', 'error')
                return redirect(url_for('main.edit_viatge', viatge_id=viatge_id))

        vehicles = Vehicle.query.join(Conductor.vehicles).filter(Conductor.usuari_id == current_user.id).all() if not current_user.super_admin else Vehicle.query.all()
        conductors = [viatge.conductor] if not current_user.super_admin else Conductor.query.all()
        parades = Parada.query.order_by(Parada.separacio_port).all()
        return render_template('viatges/editar.html', viatge=viatge, vehicles=vehicles, conductors=conductors, parades=parades)

    @staticmethod
    @login_required
    def delete_viatge(viatge_id):
        viatge = Viatge.query.get(viatge_id)
        if not viatge:
            logger.error(f"Trip ID: {viatge_id} not found")
            flash('Viatge no trobat.', 'error')
            return redirect(url_for('main.viatges'))

        if not current_user.super_admin and viatge.conductor.usuari_id != current_user.id:
            logger.warning(f"User ID: {current_user.id} attempted to delete trip ID: {viatge_id} not owned")
            flash('No tens permís per eliminar aquest viatge.', 'error')
            return redirect(url_for('main.viatges'))

        try:
            db.session.delete(viatge)
            db.session.commit()
            logger.debug(f"Deleted trip ID: {viatge_id} by user ID: {current_user.id}")
            flash('Viatge eliminat correctament!', 'success')
            return redirect(url_for('main.viatges'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting trip ID: {viatge_id}: {str(e)}")
            flash(f'Error en eliminar el viatge: {str(e)}', 'error')
            return redirect(url_for('main.viatges'))


    @staticmethod
    def update_viatges_realitzats():
        now = datetime.now()
        # Actualizar los viatges que ya han sido realizados
        viatges = Viatge.query.filter(Viatge.data_hora_inici <= now, Viatge.realitzat == False).all()
        for viatge in viatges:
            viatge.realitzat = True
        db.session.commit()
        logger.debug(f"{len(viatges)} viatges actualizados como realizados.")

