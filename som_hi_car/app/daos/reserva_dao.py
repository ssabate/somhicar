from app.daos.base_dao import BaseDAO
from app.models import Reserva
from typing import List

class ReservaDAO(BaseDAO[Reserva]):
    def add(self, reserva: Reserva) -> None:
        if not self._validate_entity(reserva):
            raise ValueError("Reserva no vàlida")
        self.db.session.add(reserva)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Reserva:
        return self.db.session.query(Reserva).filter_by(id=id).first()

    def get_all(self) -> List[Reserva]:
        # Retorna totes les reserves registrades
        return self.db.session.query(Reserva).all()

    def update(self, reserva: Reserva) -> None:
        existing = self.get_by_id(reserva.id)
        if existing:
            existing.viatge_id = reserva.viatge_id
            existing.passatger_id = reserva.passatger_id
            existing.data_reserva = reserva.data_reserva
            self.db.session.commit()

    def delete(self, reserva: Reserva) -> None:
        existing = self.get_by_id(reserva.id)
        if existing:
            self.db.session.delete(existing)
            self.db.session.commit()

    def _validate_entity(self, reserva: Reserva) -> bool:
        # ha de tenir viatge i passatgers associats
        return bool(reserva.viatge_id and reserva.passatger_id)
