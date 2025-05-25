from app.daos.base_dao import BaseDAO
from app.models import Passatger
from typing import List
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class PassatgerDAO(BaseDAO[Passatger]):
    def add(self, passatger: Passatger, commit=True) -> None:
        if not self._validate_entity(passatger):
            raise ValueError("Passatger no vàlid")
        try:
            self.db.session.add(passatger)
            if commit:
                self.db.session.commit()
            else:
                self.db.session.flush()
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error adding passatger: {str(e)}")
            raise e

    def get_by_id(self, id: int) -> Passatger:
        return self.db.session.query(Passatger).filter_by(id=id).first()

    def get_all(self) -> List[Passatger]:
        return self.db.session.query(Passatger).all()

    def update(self, passatger: Passatger) -> None:
        existing_passatger = self.get_by_id(passatger.id)
        if existing_passatger:
            existing_passatger.usuari_id = passatger.usuari_id
            existing_passatger.vegades_impuntuals = passatger.vegades_impuntuals
            existing_passatger.vegades_no_presentat = passatger.vegades_no_presentat
            existing_passatger.necessita_seient_davanter = passatger.necessita_seient_davanter
            self.db.session.commit()
        else:
            logger.error(f"Passatger ID {passatger.id} not found")
            raise ValueError("Passatger no trobat")

    def delete(self, passatger: Passatger) -> None:
        existing_passatger = self.get_by_id(passatger.id)
        if existing_passatger:
            self.db.session.delete(existing_passatger)
            self.db.session.commit()
        else:
            logger.error(f"Passatger ID {passatger.id} not found")
            raise ValueError("Passatger no trobat")

    def _validate_entity(self, passatger: Passatger) -> bool:
        return passatger.usuari_id is not None