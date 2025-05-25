from app.daos.base_dao import BaseDAO
from app.models import TipusVehicle
from typing import List

class TipusVehicleDAO(BaseDAO[TipusVehicle]):
    def add(self, tipus_vehicle: TipusVehicle) -> None:
        if not self._validate_entity(tipus_vehicle):
            raise ValueError("Tipus de vehicle no vàlid")
        self.db.session.add(tipus_vehicle)
        self.db.session.commit()

    def get_by_id(self, id: int) -> TipusVehicle:
        return self.db.session.query(TipusVehicle).filter_by(id=id).first()

    def get_all(self) -> List[TipusVehicle]:
        return self.db.session.query(TipusVehicle).all()

    def update(self, tipus_vehicle: TipusVehicle) -> None:
        existing = self.get_by_id(tipus_vehicle.id)
        if existing:
            # Actualitzem el nom
            existing.nom = tipus_vehicle.nom
            self.db.session.commit()

    def delete(self, tipus_vehicle: TipusVehicle) -> None:
        existing = self.get_by_id(tipus_vehicle.id)
        if existing:
            self.db.session.delete(existing)
            self.db.session.commit()

    def _validate_entity(self, tipus_vehicle: TipusVehicle) -> bool:
        # El nom no pot ser buit
        return bool(tipus_vehicle.nom)
