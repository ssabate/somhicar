import logging
from app import create_app
from app.daos.ubicacio_dao import UbicacioDAO
from app.models import Ubicacio, Sector
from database.db import db

logging.basicConfig(level=logging.INFO)

def test_ubicacio_dao():
    app = create_app()
    with app.app_context():
        try:
            ubicacio_dao = UbicacioDAO(db)
            sector = Sector(descripcio="Zona centre", es_port=False)
            db.session.add(sector)
            db.session.commit()

            new_ubicacio = Ubicacio(nom="Port", sector_id=sector.id)
            ubicacio_dao.add(new_ubicacio)
            logging.info(f"Ubicació creada: {new_ubicacio.nom}, ID: {new_ubicacio.id}")
            assert new_ubicacio.id is not None

            found_ubicacio = ubicacio_dao.get_by_id(new_ubicacio.id)
            logging.info(f"Ubicació trobada: {found_ubicacio.nom}")
            assert found_ubicacio.nom == "Port"

            all_ubicacions = ubicacio_dao.get_all()
            logging.info(f"Ubicacions totals: {len(all_ubicacions)}")
            assert len(all_ubicacions) > 0

            found_ubicacio.nom = "Port Modificat"
            ubicacio_dao.update(found_ubicacio)
            updated_ubicacio = ubicacio_dao.get_by_id(found_ubicacio.id)
            logging.info(f"Ubicació actualitzada: {updated_ubicacio.nom}")
            assert updated_ubicacio.nom == "Port Modificat"

            ubicacio_dao.delete(found_ubicacio)
            deleted_ubicacio = ubicacio_dao.get_by_id(found_ubicacio.id)
            logging.info(f"Ubicació eliminada: {deleted_ubicacio is None}")
            assert deleted_ubicacio is None

            logging.info("Totes les proves del UbicacioDAO completades!")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise
        finally:
            db.session.rollback()

if __name__ == "__main__":
    test_ubicacio_dao()