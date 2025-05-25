import logging
from app import create_app
from app.daos.sector_dao import SectorDAO
from app.models import Sector, Ubicacio
from database.db import db

logging.basicConfig(level=logging.INFO)

def test_sector_dao():
    app = create_app()
    with app.app_context():
        try:
            sector_dao = SectorDAO(db)
            new_sector = Sector(descripcio="Zona centre", es_port=False)
            sector_dao.add(new_sector)
            logging.info(f"Sector creat: {new_sector.descripcio}, ID: {new_sector.id}")
            assert new_sector.id is not None

            found_sector = sector_dao.get_by_id(new_sector.id)
            logging.info(f"Sector trobat: {found_sector.descripcio}")
            assert found_sector.descripcio == "Zona centre"

            all_sectors = sector_dao.get_all()
            logging.info(f"Sectors totals: {len(all_sectors)}")
            assert len(all_sectors) > 0

            found_sector.descripcio = "Centre Modificat"
            sector_dao.update(found_sector)
            updated_sector = sector_dao.get_by_id(found_sector.id)
            logging.info(f"Sector actualitzat: {updated_sector.descripcio}")
            assert updated_sector.descripcio == "Centre Modificat"

            new_ubicacio = Ubicacio(nom="Port", sector_id=new_sector.id)
            db.session.add(new_ubicacio)
            db.session.commit()
            logging.info(f"Ubicació creada: {new_ubicacio.nom}")
            assert len(found_sector.ubicacions) == 1

            sector_dao.delete(found_sector)
            deleted_sector = sector_dao.get_by_id(found_sector.id)
            logging.info(f"Sector eliminat: {deleted_sector is None}")
            assert deleted_sector is None

            logging.info("Totes les proves del SectorDAO completades!")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise
        finally:
            db.session.rollback()

if __name__ == "__main__":
    test_sector_dao()