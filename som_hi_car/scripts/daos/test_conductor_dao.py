import logging
from app import create_app
from app.daos.conductor_dao import ConductorDAO
from app.models import Conductor, Usuari, Ubicacio, Sector
from datetime import datetime
from database.db import db

logging.basicConfig(level=logging.INFO)

def test_conductor_dao():
    app = create_app()
    with app.app_context():
        try:
            conductor_dao = ConductorDAO(db)
            sector = Sector(descripcio="Zona centre", es_port=False)
            ubicacio = Ubicacio(nom="Port", sector_id=sector.id)
            usuari = Usuari(
                nom_usuari="conductor1",
                contrasenya="pass123",
                nom_complet="Anna López",
                telefon_mobil="987654321",
                ubicacio_id=ubicacio.id,
                data_naixement=datetime(1985, 5, 5)
            )
            db.session.add(sector)
            db.session.add(ubicacio)
            db.session.add(usuari)
            db.session.commit()

            new_conductor = Conductor(
                usuari_id=usuari.id,
                carnet_categoria_superior="C",
                accidents_tinguts=0
            )
            conductor_dao.add(new_conductor)
            logging.info(f"Conductor creat: ID: {new_conductor.id}")
            assert new_conductor.id is not None

            found_conductor = conductor_dao.get_by_id(new_conductor.id)
            logging.info(f"Conductor trobat: Carnet: {found_conductor.carnet_categoria_superior}")
            assert found_conductor.carnet_categoria_superior == "C"

            all_conductors = conductor_dao.get_all()
            logging.info(f"Conductors totals: {len(all_conductors)}")
            assert len(all_conductors) > 0

            found_conductor.carnet_categoria_superior = "D"
            conductor_dao.update(found_conductor)
            updated_conductor = conductor_dao.get_by_id(found_conductor.id)
            logging.info(f"Conductor actualitzat: Carnet: {updated_conductor.carnet_categoria_superior}")
            assert updated_conductor.carnet_categoria_superior == "D"

            conductor_dao.delete(found_conductor)
            deleted_conductor = conductor_dao.get_by_id(found_conductor.id)
            logging.info(f"Conductor eliminat: {deleted_conductor is None}")
            assert deleted_conductor is None

            logging.info("Totes les proves del ConductorDAO completades!")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise
        finally:
            db.session.rollback()

if __name__ == "__main__":
    test_conductor_dao()