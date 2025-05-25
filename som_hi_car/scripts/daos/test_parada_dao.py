# tests/test_parada_dao.py
import logging
from app import create_app
from app.daos.parada_dao import ParadaDAO
from app.models import Parada, Ubicacio, Sector
from database.db import db

logging.basicConfig(level=logging.INFO)

def test_parada_dao():
    app = create_app()
    with app.app_context():
        try:
            parada_dao = ParadaDAO(db)
            sector = Sector(descripcio="Zona centre", es_port=False)
            ubicacio = Ubicacio(nom="Port", sector_id=sector.id)
            db.session.add(sector)
            db.session.add(ubicacio)
            db.session.commit()

            new_parada = Parada(descripcio="Parada 1", ubicacio_id=ubicacio.id, separacio_port=100)
            parada_dao.add(new_parada)
            logging.info(f"Parada creada: {new_parada.descripcio}, ID: {new_parada.id}")
            assert new_parada.id is not None

            found_parada = parada_dao.get_by_id(new_parada.id)
            logging.info(f"Parada trobada: {found_parada.descripcio}")
            assert found_parada.descripcio == "Parada 1"

            all_parades = parada_dao.get_all()
            logging.info(f"Parades totals: {len(all_parades)}")
            assert len(all_parades) > 0

            found_parada.descripcio = "Parada 1 Modificada"
            parada_dao.update(found_parada)
            updated_parada = parada_dao.get_by_id(found_parada.id)
            logging.info(f"Parada actualitzada: {updated_parada.descripcio}")
            assert updated_parada.descripcio == "Parada 1 Modificada"

            parada_dao.delete(found_parada)
            deleted_parada = parada_dao.get_by_id(found_parada.id)
            logging.info(f"Parada eliminada: {deleted_parada is None}")
            assert deleted_parada is None

            logging.info("Totes les proves del ParadaDAO completades!")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise
        finally:
            db.session.rollback()

if __name__ == "__main__":
    test_parada_dao()