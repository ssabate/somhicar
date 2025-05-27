from flask import flash, redirect, url_for, render_template, current_app
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.daos.usuari_dao import UsuariDAO
from app.daos.passatger_dao import PassatgerDAO  # Import PassatgerDAO
from app.forms.auth_forms import RegisterForm, LoginForm
from app.models import Usuari, Passatger
from sqlalchemy.exc import IntegrityError, DataError
import traceback

class AuthController:
    @staticmethod
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('main.perfil'))
        form = RegisterForm()
        if form.validate_on_submit():
            nom_usuari = form.nom_usuari.data
            email = form.email.data
            phone = form.phone.data
            password = form.password.data
            data_naixement = form.data_naixement.data
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            usuari = Usuari(
                nom_usuari=nom_usuari,
                email=email,
                contrasenya=hashed_password,
                nom_complet=nom_usuari,
                telefon_mobil=phone,
                data_naixement=data_naixement
            )
            with current_app.app_context():
                from database.db import db
                current_app.logger.debug(f"db.session available in register: {hasattr(db, 'session')}")
                try:
                    user_dao = UsuariDAO(db)
                    passatger_dao = PassatgerDAO(db)  # Initialize PassatgerDAO
                    # Validate uniqueness of nom_usuari, email, and phone
                    if user_dao.get_by_nom_usuari(nom_usuari):
                        flash('Aquest nom d\'usuari ja està registrat. Prova amb un altre.', 'error')
                        return render_template('auth/register.html', form=form)
                    if user_dao.get_by_email(email):
                        flash('Aquest correu electrònic ja està registrat. Prova amb un altre.', 'error')
                        return render_template('auth/register.html', form=form)
                    if user_dao.get_by_phone(phone):
                        flash('Aquest número de telèfon ja està registrat. Prova amb un altre.', 'error')
                        return render_template('auth/register.html', form=form)

                    # Add user and passenger in the same transaction
                    db.session.add(usuari)
                    db.session.flush()  # Force ID assignment without commit
                    current_app.logger.debug(f"Usuari ID after flush: {usuari.id}")
                    passatger = Passatger(
                        usuari_id=usuari.id,
                        vegades_impuntuals=0,
                        vegades_no_presentat=0,
                        necessita_seient_davanter=False
                    )
                    passatger_dao.add(passatger)  # Use PassatgerDAO for consistency
                    db.session.commit()
                    flash('Registre completat amb èxit! Pots iniciar sessió.', 'success')
                    return redirect(url_for('auth.login'))
                except ValueError as e:
                    db.session.rollback()
                    flash(f'Error en el registre: {str(e)}', 'error')
                    current_app.logger.error(f"ValueError in register: {str(e)}\n{traceback.format_exc()}")
                except IntegrityError as e:
                    db.session.rollback()
                    flash('Error en el registre: dades duplicades o invàlides. Comprova els camps.', 'error')
                    current_app.logger.error(f"IntegrityError in register: {str(e)}\n{traceback.format_exc()}")
                except DataError as e:
                    db.session.rollback()
                    flash('Error en el registre: algunes dades són invàlides (per exemple, camps massa llargs).', 'error')
                    current_app.logger.error(f"DataError in register: {str(e)}\n{traceback.format_exc()}")
                except Exception as e:
                    db.session.rollback()
                    flash('Error inesperat en el registre. Si us plau, intenta-ho de nou més tard.', 'error')
                    current_app.logger.error(f"Unexpected error in register: {str(e)}\n{traceback.format_exc()}")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en {getattr(form, field).label.text}: {error}", 'error')
                current_app.logger.debug(f"Form error in {field}: {error}")
        return render_template('auth/register.html', form=form)

    @staticmethod
    def login():
        if current_user.is_authenticated:
            # return redirect(url_for('main.perfil'))
            return redirect(url_for('main.reserves'))
        form = LoginForm()
        if form.validate_on_submit():
            identifier = form.identifier.data
            password = form.password.data
            with current_app.app_context():
                from database.db import db
                current_app.logger.debug(f"db.session available in login: {hasattr(db, 'session')}")
                try:
                    user_dao = UsuariDAO(db)
                    user = user_dao.get_by_email(identifier) or user_dao.get_by_nom_usuari(identifier)
                    if user and check_password_hash(user.contrasenya, password):
                        login_user(user)
                        flash('Has iniciat sessió amb èxit!', 'success')
                        return redirect(url_for('main.reserves'))
                        # return redirect(url_for('main.perfil'))
                    else:
                        flash('Correu electrònic, nom d\'usuari o contrasenya incorrectes.', 'error')
                except Exception as e:
                    current_app.logger.error(f"Error in login: {str(e)}\n{traceback.format_exc()}")
                    flash('Error inesperat en l\'inici de sessió. Si us plau, intenta-ho de nou.', 'error')
        return render_template('auth/login.html', form=form)

    @staticmethod
    def logout():
        logout_user()
        flash('Has tancat sessió amb èxit.', 'success')
        return redirect(url_for('auth.login'))