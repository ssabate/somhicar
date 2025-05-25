from app.daos.base_dao import BaseDAO
from app.models import Ubicacio
from typing import List

class UbicacioDAO(BaseDAO[Ubicacio]):
    def add(self, ubicacio: Ubicacio) -> None:
        if not self._validate_entity(ubicacio):
            raise ValueError("Ubicació no vàlida")
        self.db.session.add(ubicacio)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Ubicacio:
        return self.db.session.query(Ubicacio).filter_by(id=id).first()

    def get_all(self) -> List[Ubicacio]:
        return self.db.session.query(Ubicacio).all()

    def update(self, ubicacio: Ubicacio) -> None:
        existing_ubicacio = self.get_by_id(ubicacio.id)
        if existing_ubicacio:
            existing_ubicacio.nom = ubicacio.nom
            existing_ubicacio.sector_id = ubicacio.sector_id
            self.db.session.commit()

    def delete(self, ubicacio: Ubicacio) -> None:
        existing_ubicacio = self.get_by_id(ubicacio.id)
        if existing_ubicacio:
            self.db.session.delete(existing_ubicacio)
            self.db.session.commit()

    def _validate_entity(self, ubicacio: Ubicacio) -> bool:
        return (
            ubicacio.nom is not None and len(ubicacio.nom) > 0 and
            ubicacio.sector_id is not None  # La clau forana sector_id és obligatòria
        )