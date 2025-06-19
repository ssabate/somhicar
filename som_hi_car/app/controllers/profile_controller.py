from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import current_user, login_required
from app.daos.usuari_dao import UsuariDAO
from app.daos.vehicle_dao import VehicleDAO
from app.daos.conductor_dao import ConductorDAO
from app.forms.profile_forms import ProfileForm
from app.forms.vehicle_forms import VehicleForm
from database.db import db
from app.models import Viatge, Reserva, Vehicle, Conductor, TipusVehicle
import os
from werkzeug.utils import secure_filename
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProfileController:

    @staticmethod
    def show_terms():
        logger.debug("Showing terms and conditions")
        return render_template('legislacio/AvisLegal.html')

    @staticmethod
    def show_policy():
        logger.debug("Showing privacy policy")
        return render_template('legislacio/Politica_privacitat.html')

    @staticmethod
    @login_required
    def show_profile():
        user_dao = UsuariDAO(db)
        user = user_dao.get_by_id(current_user.id)
        logger.debug(f"Showing profile for user ID: {user.id}, Email: {user.email}")

        # Crear formulario con datos actuales
        form = ProfileForm(
            nom=user.nom_complet.split()[0] if user.nom_complet else '',
            cognom=' '.join(user.nom_complet.split()[1:]) if user.nom_complet else '',
            email=user.email,
            telefon_mobil=user.telefon_mobil,
            telefon_fix=user.telefon_fix,
            adreca=user.adreca,
            data_naixement=user.data_naixement,
            ubicacio_id=user.ubicacio_id or 0
        )

        # Query trips where user is conductor
        conductor_trips = Viatge.query.filter(Viatge.conductor.has(usuari_id=current_user.id)).all()
        # Query trips where user is passenger
        passenger_trips = Viatge.query.join(Reserva).filter(Reserva.passatger.has(usuari_id=current_user.id)).all()
        # Combine and remove duplicates, sort by data_hora_inici descending
        trips = sorted(list(set(conductor_trips + passenger_trips)), key=lambda x: x.data_hora_inici, reverse=True)
        logger.debug(f"Found {len(trips)} trips for user ID: {user.id}")

        return render_template('profile.html', user=user, form=form, trips=trips)

    @staticmethod
    @login_required
    def update_profile():
        user_dao = UsuariDAO(db)
        user = user_dao.get_by_id(current_user.id)
        form = ProfileForm()
        logger.debug(f"Processing update_profile for user ID: {user.id}")

        if form.validate_on_submit():
            logger.debug("Form validated successfully")
            try:
                # Actualizar datos del usuario
                user.nom_complet = f"{form.nom.data} {form.cognom.data}".strip()
                user.email = form.email.data
                user.telefon_mobil = form.telefon_mobil.data
                user.telefon_fix = form.telefon_fix.data
                user.adreca = form.adreca.data
                user.data_naixement = form.data_naixement.data
                user.ubicacio_id = form.ubicacio_id.data if form.ubicacio_id.data != 0 else None
                user.confirmation_needed = bool(form.confirmation_needed.data)

                # Handle avatar upload
                if form.avatar.data:
                    logger.debug(f"Processing avatar upload: {form.avatar.data.filename}")
                    # Generate a unique filename
                    filename = secure_filename(form.avatar.data.filename)
                    ext = os.path.splitext(filename)[1]
                    unique_filename = f"{uuid.uuid4().hex}{ext}"
                    # Use absolute path for UPLOAD_FOLDER
                    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
                    upload_path = os.path.join(upload_folder, unique_filename)

                    # Ensure upload directory exists and is writable
                    logger.debug(f"Upload folder: {upload_folder}")
                    os.makedirs(upload_folder, exist_ok=True)
                    if not os.access(upload_folder, os.W_OK):
                        logger.error(f"No write permissions for {upload_folder}")
                        raise PermissionError(f"No write permissions for {upload_folder}")

                    # Save the file
                    try:
                        form.avatar.data.save(upload_path)
                        logger.debug(f"Avatar saved to: {upload_path}")
                        # Verify file exists
                        if not os.path.exists(upload_path):
                            logger.error(f"File not saved at {upload_path}")
                            raise IOError(f"Failed to save file at {upload_path}")
                    except Exception as e:
                        logger.error(f"Error saving avatar: {str(e)}")
                        raise

                    # Update user's avatar filename
                    user.avatar = unique_filename
                    logger.debug(f"User avatar updated to: {unique_filename}")

                # Update password if provided
                if form.nova_contrasenya.data:
                    from werkzeug.security import generate_password_hash
                    user.contrasenya = generate_password_hash(form.nova_contrasenya.data)
                    logger.debug("Password updated")

                logger.debug(f"Updating user: {user.nom_complet}, {user.email}, {user.ubicacio_id}")
                user_dao.update(user)
                db.session.commit()
                logger.debug("Database commit successful")
                flash('Perfil actualitzat correctament!', 'success')
                return redirect(url_for('main.perfil'))

            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating profile: {str(e)}")
                flash(f'Error en actualitzar el perfil: {str(e)}', 'error')

        else:
            logger.debug(f"Form validation failed: {form.errors}")
            flash('Hi ha errors en el formulari. Revisa els camps.', 'error')

        # Pass empty trips list to avoid template errors
        return render_template('profile.html', user=user, form=form, trips=[])

    @staticmethod
    @login_required
    def create_vehicle():
        vehicle_dao = VehicleDAO(db)
        conductor_dao = ConductorDAO(db)
        form = VehicleForm()
        logger.debug(f"Processing create_vehicle for user ID: {current_user.id}")

        # Fetch vehicle types and set form choices
        tipus_vehicles = TipusVehicle.query.all()
        if not tipus_vehicles:
            logger.warning("No vehicle types found in tipus_vehicles table")
            flash('No hi ha tipus de vehicles disponibles. Contacta amb l’administrador.', 'error')
            return redirect(url_for('main.perfil'))

        # Set choices for tipus_vehicle_id
        form.tipus_vehicle_id.choices = [(tv.id, tv.nom) for tv in tipus_vehicles]
        logger.debug(f"Set {len(tipus_vehicles)} vehicle type choices: {[(tv.id, tv.nom) for tv in tipus_vehicles]}")

        if request.method == 'POST':
            if form.validate_on_submit():
                logger.debug("Vehicle form validated successfully")
                try:
                    # Check for duplicate matricula
                    if Vehicle.query.filter_by(matricula=form.matricula.data).first():
                        logger.error(f"Duplicate matricula: {form.matricula.data}")
                        flash('Aquesta matrícula ja està registrada.', 'error')
                        return render_template('vehicles/nou_user.html', form=form, tipus_vehicles=tipus_vehicles)

                    # Create vehicle
                    vehicle = Vehicle(
                        matricula=form.matricula.data,
                        marca=form.marca.data,
                        model=form.model.data,
                        color=form.color.data or '',
                        num_places=form.num_places.data,
                        tipus_vehicle_id=form.tipus_vehicle_id.data
                    )
                    vehicle_dao.add(vehicle)
                    logger.debug(f"Vehicle created: {vehicle.matricula}")

                    # Check if user is already a conductor
                    conductor = Conductor.query.filter_by(usuari_id=current_user.id).first()
                    if not conductor:
                        # Create conductor record
                        conductor = Conductor(
                            usuari_id=current_user.id,
                            carnet_categoria_superior='B',
                            accidents_tinguts=0
                        )

                        conductor_dao.add(conductor)
                        logger.debug(f"Conductor created for user ID: {current_user.id}")

                    # Associate vehicle with conductor
                    conductor.vehicles.append(vehicle)
                    db.session.commit()
                    logger.debug(f"Vehicle {vehicle.matricula} associated with conductor ID: {conductor.id}")

                    flash('Vehicle afegit correctament! Ara pots crear viatges.', 'success')
                    return redirect(url_for('main.perfil'))

                except Exception as e:
                    db.session.rollback()
                    logger.error(f"Error creating vehicle: {str(e)}")
                    flash(f'Error en afegir el vehicle: {str(e)}', 'error')
            else:
                logger.debug(f"Vehicle form validation failed: {form.errors}")
                flash('Hi ha errors en el formulari. Revisa els camps.', 'error')

        return render_template('vehicles/nou_user.html', form=form, tipus_vehicles=tipus_vehicles)