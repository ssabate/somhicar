from app.daos.base_dao import BaseDAO
from app.models import Viatge
from typing import List

class ViatgeDAO(BaseDAO[Viatge]):
    def add(self, viatge: Viatge) -> None:
        if not self._validate_entity(viatge):
            raise ValueError("Viatge no vàlid")
        self.db.session.add(viatge)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Viatge:
        return self.db.session.query(Viatge).filter_by(id=id).first()

    def get_all(self) -> List[Viatge]:
        return self.db.session.query(Viatge).all()

    def update(self, viatge: Viatge) -> None:
        existing = self.get_by_id(viatge.id)
        if existing:
            existing.data_hora_inici = viatge.data_hora_inici
            existing.places_inicials = viatge.places_inicials
            existing.places_restants = viatge.places_restants
            existing.vehicle_id = viatge.vehicle_id
            existing.conductor_id = viatge.conductor_id
            existing.parada_recollida_id = viatge.parada_recollida_id
            existing.parada_arribada_id = viatge.parada_arribada_id
            existing.sentit = viatge.sentit
            existing.import_ = viatge.import_
            existing.confirmat = viatge.confirmat
            existing.realitzat = viatge.realitzat
            self.db.session.commit()

    def delete(self, viatge: Viatge) -> None:
        existing = self.get_by_id(viatge.id)
        if existing:
            self.db.session.delete(existing)
            self.db.session.commit()

    def _validate_entity(self, viatge: Viatge) -> bool:
        return bool(viatge.data_hora_inici and viatge.parada_recollida_id and viatge.parada_arribada_id)