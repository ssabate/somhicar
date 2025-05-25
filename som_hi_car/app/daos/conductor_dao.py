from app.daos.base_dao import BaseDAO
from app.models import Conductor
from typing import List

class ConductorDAO(BaseDAO[Conductor]):
    def add(self, conductor: Conductor) -> None:
        if not self._validate_entity(conductor):
            raise ValueError("Conductor no vàlid")
        self.db.session.add(conductor)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Conductor:
        return self.db.session.query(Conductor).filter_by(id=id).first()

    def get_all(self) -> List[Conductor]:
        return self.db.session.query(Conductor).all()

    def update(self, conductor: Conductor) -> None:
        existing_conductor = self.get_by_id(conductor.id)
        if existing_conductor:
            existing_conductor.usuari_id = conductor.usuari_id
            existing_conductor.carnet_categoria_superior = conductor.carnet_categoria_superior
            existing_conductor.accidents_tinguts = conductor.accidents_tinguts
            self.db.session.commit()

    def delete(self, conductor: Conductor) -> None:
        existing_conductor = self.get_by_id(conductor.id)
        if existing_conductor:
            self.db.session.delete(existing_conductor)
            self.db.session.commit()

    def _validate_entity(self, conductor: Conductor) -> bool:
        return conductor.usuari_id is not None