from app.daos.base_dao import BaseDAO
from app.models import Configuracio
from typing import List
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class ConfiguracioDAO(BaseDAO[Configuracio]):
    def __init__(self, db):
        super().__init__(db)
        if not hasattr(self.db, 'session'):
            raise AttributeError("Database object is not properly initialized with a session")
        logging.debug(f"ConfiguracioDAO initialized with db type: {type(self.db)}")

    def add(self, config: Configuracio) -> None:
        if not self._validate_entity(config):
            raise ValueError("Configuració no vàlida: alguns camps obligatoris són buits o invàlids")
        with current_app.app_context():
            try:
                self.db.session.add(config)
                self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                logging.error(f"Error adding configuration: {str(e)}")
                raise e

    def get_by_id(self, id: int) -> Configuracio:
        logger.debug(f"Fetching config by ID: {id}")
        return self.db.session.query(Configuracio).filter_by(id=id).first()

    def get_all(self) -> List[Configuracio]:
        with current_app.app_context():
            try:
                return self.db.session.query(Configuracio).all()
            except Exception as e:
                logging.error(f"Error getting all configuration: {str(e)}")
                raise e

    def update(self, config: Configuracio) -> None:
        logger.debug(f"Updating configuration ID: {config.id}")
        existing_config = self.get_by_id(config.id)
        if existing_config:
            # Update fields
            existing_config.pagament_activat = config.pagament_activat
            logger.debug(f"Config fields updated: {existing_config.id}")
            self.db.session.commit()
            logger.debug("Config update committed")
        else:
            logger.error(f"Config ID {config.id} not found")
            raise ValueError("Configuració no trobada")

    def delete(self, config: Configuracio) -> None:
        with current_app.app_context():
            try:
                existing_config = self.get_by_id(config.id)
                if existing_config:
                    self.db.session.delete(existing_config)
                    self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                logging.error(f"Error deleting configuration: {str(e)}")
                raise e

    def _validate_entity(self, config: Configuracio) -> bool:
        return (
            config.pagament_activat is not None and (config.pagament_activat == True .nom_usuari or config.pagament_activat == False )
        )