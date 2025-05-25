from app.daos.base_dao import BaseDAO
from app.models import Usuari
from typing import List
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class UsuariDAO(BaseDAO[Usuari]):
    def __init__(self, db):
        super().__init__(db)
        if not hasattr(self.db, 'session'):
            raise AttributeError("Database object is not properly initialized with a session")
        logging.debug(f"UsuariDAO initialized with db type: {type(self.db)}")

    def add(self, usuari: Usuari) -> None:
        if not self._validate_entity(usuari):
            raise ValueError("Usuari no vàlid: alguns camps obligatoris són buits o invàlids")
        with current_app.app_context():
            try:
                self.db.session.add(usuari)
                self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                logging.error(f"Error adding user: {str(e)}")
                raise e

    def get_by_id(self, id: int) -> Usuari:
        logger.debug(f"Fetching user by ID: {id}")
        return self.db.session.query(Usuari).filter_by(id=id).first()

    def get_by_email(self, email: str) -> Usuari:
        with current_app.app_context():
            try:
                return self.db.session.query(Usuari).filter_by(email=email).first()
            except Exception as e:
                logging.error(f"Error getting user by email {email}: {str(e)}")
                raise e

    def get_by_phone(self, phone: str) -> Usuari:
        with current_app.app_context():
            try:
                return self.db.session.query(Usuari).filter_by(telefon_mobil=phone).first()
            except Exception as e:
                logging.error(f"Error getting user by phone {phone}: {str(e)}")
                raise e

    def get_by_nom_usuari(self, nom_usuari: str) -> Usuari:
        with current_app.app_context():
            try:
                return self.db.session.query(Usuari).filter_by(nom_usuari=nom_usuari).first()
            except Exception as e:
                logging.error(f"Error getting user by nom_usuari {nom_usuari}: {str(e)}")
                raise e

    def get_all(self) -> List[Usuari]:
        with current_app.app_context():
            try:
                return self.db.session.query(Usuari).all()
            except Exception as e:
                logging.error(f"Error getting all users: {str(e)}")
                raise e

    def update(self, usuari: Usuari) -> None:
        logger.debug(f"Updating user ID: {usuari.id}, Email: {usuari.email}")
        existing_usuari = self.get_by_id(usuari.id)
        if existing_usuari:
            # Update fields
            existing_usuari.nom_usuari = usuari.nom_usuari
            existing_usuari.contrasenya = usuari.contrasenya
            existing_usuari.nom_complet = usuari.nom_complet
            existing_usuari.email = usuari.email
            existing_usuari.telefon_fix = usuari.telefon_fix
            existing_usuari.telefon_mobil = usuari.telefon_mobil
            existing_usuari.adreca = usuari.adreca
            existing_usuari.ubicacio_id = usuari.ubicacio_id
            existing_usuari.data_naixement = usuari.data_naixement
            existing_usuari.avatar = usuari.avatar
            logger.debug(f"User fields updated: {existing_usuari.nom_complet}")
            self.db.session.commit()
            logger.debug("User update committed")
        else:
            logger.error(f"User ID {usuari.id} not found")
            raise ValueError("Usuari no trobat")

    def delete(self, usuari: Usuari) -> None:
        with current_app.app_context():
            try:
                existing_usuari = self.get_by_id(usuari.id)
                if existing_usuari:
                    self.db.session.delete(existing_usuari)
                    self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                logging.error(f"Error deleting user: {str(e)}")
                raise e

    def _validate_entity(self, usuari: Usuari) -> bool:
        return (
            usuari.nom_usuari is not None and len(usuari.nom_usuari) > 0 and
            usuari.contrasenya is not None and len(usuari.contrasenya) > 0 and
            usuari.nom_complet is not None and len(usuari.nom_complet) > 0 and
            usuari.email is not None and len(usuari.email) > 0
        )