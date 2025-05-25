from app.daos.base_dao import BaseDAO
from app.models import Sector
from typing import List

class SectorDAO(BaseDAO[Sector]):
    def add(self, sector: Sector) -> None:
        if not self._validate_entity(sector):
            raise ValueError("Sector no vàlid")
        self.db.session.add(sector)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Sector:
        return self.db.session.query(Sector).filter_by(id=id).first()

    def get_all(self) -> List[Sector]:
        return self.db.session.query(Sector).all()

    def update(self, sector: Sector) -> None:
        existing_sector = self.get_by_id(sector.id)
        if existing_sector:
            existing_sector.descripcio = sector.descripcio
            existing_sector.es_port = sector.es_port
            self.db.session.commit()

    def delete(self, sector: Sector) -> None:
        existing_sector = self.get_by_id(sector.id)
        if existing_sector:
            self.db.session.delete(existing_sector)
            self.db.session.commit()

    def _validate_entity(self, sector: Sector) -> bool:
        return sector.descripcio is not None and len(sector.descripcio) > 0