from app.daos.base_dao import BaseDAO
from app.models import Parada
from typing import List

class ParadaDAO(BaseDAO[Parada]):
    def add(self, parada: Parada) -> None:
        if not self._validate_entity(parada):
            raise ValueError("Parada no vàlida")
        self.db.session.add(parada)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Parada:
        return self.db.session.query(Parada).filter_by(id=id).first()

    def get_all(self) -> List[Parada]:
        return self.db.session.query(Parada).all()

    def update(self, parada: Parada) -> None:
        existing_parada = self.get_by_id(parada.id)
        if existing_parada:
            existing_parada.descripcio = parada.descripcio
            existing_parada.ubicacio_id = parada.ubicacio_id
            existing_parada.separacio_port = parada.separacio_port
            self.db.session.commit()

    def delete(self, parada: Parada) -> None:
        existing_parada = self.get_by_id(parada.id)
        if existing_parada:
            self.db.session.delete(existing_parada)
            self.db.session.commit()

    def _validate_entity(self, parada: Parada) -> bool:
        return (
            parada.descripcio is not None and len(parada.descripcio) > 0 and
            parada.ubicacio_id is not None and
            parada.separacio_port is not None and parada.separacio_port >= 0
        )