import logging
from app import create_app
from app.daos.passatger_dao import PassatgerDAO
from app.models import Passatger, Usuari, Ubicacio, Sector
from datetime import datetime
from database.db import db

logging.basicConfig(level=logging.INFO)

def test_passatger_dao():
    app = create_app()
    with app.app_context():
        try:
            passatger_dao = PassatgerDAO(db)
            sector = Sector(descripcio="Zona centre", es_port=False)
            ubicacio = Ubicacio(nom="Port", sector_id=sector.id)
            usuari = Usuari(
                nom_usuari="passatger1",
                contrasenya="pass123",
                nom_complet="Maria Gómez",
                telefon_mobil="123123123",
                ubicacio_id=ubicacio.id,
                data_naixement=datetime(1995, 10, 10)
            )
            db.session.add(sector)
            db.session.add(ubicacio)
            db.session.add(usuari)
            db.session.commit()

            new_passatger = Passatger(
                usuari_id=usuari.id,
                vegades_impuntuals=0,
                vegades_no_presentat=0,
                necessita_seient_davanter=True
            )
            passatger_dao.add(new_passatger)
            logging.info(f"Passatger creat: ID: {new_passatger.id}")
            assert new_passatger.id is not None

            found_passatger = passatger_dao.get_by_id(new_passatger.id)
            logging.info(f"Passatger trobat: Necessita seient: {found_passatger.necessita_seient_davanter}")
            assert found_passatger.necessita_seient_davanter is True

            all_passatgers = passatger_dao.get_all()
            logging.info(f"Passatgers totals: {len(all_passatgers)}")
            assert len(all_passatgers) > 0

            found_passatger.vegades_impuntuals = 1
            passatger_dao.update(found_passatger)
            updated_passatger = passatger_dao.get_by_id(found_passatger.id)
            logging.info(f"Passatger actualitzat: Impuntualitats: {updated_passatger.vegades_impuntuals}")
            assert updated_passatger.vegades_impuntuals == 1

            passatger_dao.delete(found_passatger)
            deleted_passatger = passatger_dao.get_by_id(found_passatger.id)
            logging.info(f"Passatger eliminat: {deleted_passatger is None}")
            assert deleted_passatger is None

            logging.info("Totes les proves del PassatgerDAO completades!")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise
        finally:
            db.session.rollback()

if __name__ == "__main__":
    test_passatger_dao()