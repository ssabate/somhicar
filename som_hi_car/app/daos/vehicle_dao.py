# app/daos/vehicle_dao.py
from app.daos.base_dao import BaseDAO
from app.models import Vehicle
from typing import List

class VehicleDAO(BaseDAO[Vehicle]):

    def add(self, vehicle: Vehicle) -> None:
        #Comprovem que existeix el vehicle mirant la seva matricula
        if not self._validate_entity(vehicle):
            raise ValueError("Vehicle no vàlid")
        self.db.session.add(vehicle)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Vehicle:
        return self.db.session.query(Vehicle).filter_by(id=id).first()

    def get_all(self) -> List[Vehicle]:
        return self.db.session.query(Vehicle).all()

    def update(self, vehicle: Vehicle) -> None:
        existing = self.get_by_id(vehicle.id)
        #Copiem les dades passades al registre del vehicle existent
        #No creo un nou registre sino que reemplaço una a una els camps.
        if existing:
            existing.matricula = vehicle.matricula
            existing.marca = vehicle.marca
            existing.model = vehicle.model
            existing.color = vehicle.color
            existing.num_places = vehicle.num_places
            existing.tipus_vehicle_id = vehicle.tipus_vehicle_id
            self.db.session.commit()

    def delete(self, vehicle: Vehicle) -> None:
        existing = self.get_by_id(vehicle.id)
        if existing:
            self.db.session.delete(existing)
            self.db.session.commit()

    def _validate_entity(self, vehicle: Vehicle) -> bool:
        #comprovem que la matrícula no estigue en null o buit
        return bool(vehicle.matricula)
