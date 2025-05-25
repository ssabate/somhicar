import logging
from app import create_app
from app.daos.usuari_dao import UsuariDAO
from app.models import Usuari, Ubicacio, Sector
from datetime import datetime
from database.db import db

logging.basicConfig(level=logging.INFO)

def test_usuari_dao():
    app = create_app()
    with app.app_context():
        try:
            usuari_dao = UsuariDAO(db)
            sector = Sector(descripcio="Zona centre", es_port=False)
            ubicacio = Ubicacio(nom="Port", sector_id=sector.id)
            db.session.add(sector)
            db.session.add(ubicacio)
            db.session.commit()

            new_usuari = Usuari(
                nom_usuari="user1",
                contrasenya="pass123",
                nom_complet="Joan Pérez",
                telefon_mobil="123456789",
                ubicacio_id=ubicacio.id,
                data_naixement=datetime(1990, 1, 1)
            )
            usuari_dao.add(new_usuari)
            logging.info(f"Usuari creat: {new_usuari.nom_usuari}, ID: {new_usuari.id}")
            assert new_usuari.id is not None

            found_usuari = usuari_dao.get_by_id(new_usuari.id)
            logging.info(f"Usuari trobat: {found_usuari.nom_usuari}")
            assert found_usuari.nom_usuari == "user1"

            all_usuaris = usuari_dao.get_all()
            logging.info(f"Usuaris totals: {len(all_usuaris)}")
            assert len(all_usuaris) > 0

            found_usuari.nom_complet = "Joan Pérez Modificat"
            usuari_dao.update(found_usuari)
            updated_usuari = usuari_dao.get_by_id(found_usuari.id)
            logging.info(f"Usuari actualitzat: {updated_usuari.nom_complet}")
            assert updated_usuari.nom_complet == "Joan Pérez Modificat"

            usuari_dao.delete(found_usuari)
            deleted_usuari = usuari_dao.get_by_id(found_usuari.id)
            logging.info(f"Usuari eliminat: {deleted_usuari is None}")
            assert deleted_usuari is None

            logging.info("Totes les proves del UsuariDAO completades!")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise
        finally:
            db.session.rollback()

if __name__ == "__main__":
    test_usuari_dao()