from datetime import datetime
from app.models import Sector, Ubicacio, Parada, TipusVehicle, Usuari, Conductor, Passatger, Vehicle, Configuracio
from database.db import db
from werkzeug.security import generate_password_hash

def inserta_dades_base():

    # ---- CONFIGURACIÓ ----
    configuracio = Configuracio.query.first()
    if not configuracio:
        configuracio = Configuracio(pagament_activat=True, id=1)
        db.session.add(configuracio)
    db.session.commit()

    # ---- SECTORS ----
    sectors_info = [
        {"descripcio": "Lo Port", "es_port": True},
        {"descripcio": "Reguers", "es_port": False},
        {"descripcio": "Jesús", "es_port": False},
        {"descripcio": "Roquetes", "es_port": False},
        {"descripcio": "Tortosa", "es_port": False},
        {"descripcio": "Alfara de Carles", "es_port": False},
    ]
    sectors = {}
    for s in sectors_info:
        sector = Sector.query.filter_by(descripcio=s["descripcio"]).first()
        if not sector:
            sector = Sector(descripcio=s["descripcio"], es_port=s["es_port"])
            db.session.add(sector)
        sectors[s["descripcio"]] = sector
    db.session.commit()

    # ---- UBICACIONS ----
    ubicacions_info = [
        {"nom": "Tortosa centre", "sector": sectors["Tortosa"]},
        {"nom": "Reguers poble", "sector": sectors["Reguers"]},
        {"nom": "Jesús poble", "sector": sectors["Jesús"]},
        {"nom": "Roquetes ciutat", "sector": sectors["Roquetes"]},
        {"nom": "Roquetes rodalies", "sector": sectors["Roquetes"]},
        {"nom": "Alfara de Carles poble", "sector": sectors["Alfara de Carles"]},
        {"nom": "Lo Port", "sector": sectors["Lo Port"]},
    ]
    ubicacions = {}
    for u in ubicacions_info:
        ubicacio = Ubicacio.query.filter_by(nom=u["nom"]).first()
        if not ubicacio:
            ubicacio = Ubicacio(nom=u["nom"], sector=u["sector"])
            db.session.add(ubicacio)
        ubicacions[u["nom"]] = ubicacio
    db.session.commit()

    # ---- PARADES ----
    parades_info = [
        {"descripcio": "L'Esquirol (rest. La Tele)", "ubicacio": ubicacions["Lo Port centre"], "separacio_port": 0},
        {"descripcio": "Pous de la Neu (cruïlla camí Caro)", "ubicacio": ubicacions["Lo Port centre"], "separacio_port": 0},
        {"descripcio": "Pous de la Neu (restaurant)", "ubicacio": ubicacions["Lo Port centre"], "separacio_port": 0},
        {"descripcio": "Urbanització Els Pilans", "ubicacio": ubicacions["Roquetes rodalies"], "separacio_port": 15},
        {"descripcio": "Reguers centre", "ubicacio": ubicacions["Reguers poble"], "separacio_port": 17},
        {"descripcio": "Jesús mercat", "ubicacio": ubicacions["Jesús poble"], "separacio_port": 20},
        {"descripcio": "Tortosa mercat", "ubicacio": ubicacions["Tortosa centre"], "separacio_port": 25},
        {"descripcio": "Roquetes mercat", "ubicacio": ubicacions["Roquetes ciutat"], "separacio_port": 20},
    ]
    for p in parades_info:
        parada = Parada.query.filter_by(descripcio=p["descripcio"]).first()
        if not parada:
            parada = Parada(descripcio=p["descripcio"], ubicacio=p["ubicacio"], separacio_port=p["separacio_port"])
            db.session.add(parada)
    db.session.commit()

    # ---- TIPUS DE VEHICLES ----
    tipus_vehicle_names = ["Cotxe", "Moto", "Furgoneta", "Bicicleta"]
    tipus_vehicles = {}
    for nom in tipus_vehicle_names:
        tipus = TipusVehicle.query.filter_by(nom=nom).first()
        if not tipus:
            tipus = TipusVehicle(nom=nom)
            db.session.add(tipus)
        tipus_vehicles[nom] = tipus
    db.session.commit()

    # ---- USUARIS, PASSATGERS I CONDUCTORS ----
    # Usuari: Jordi (Passatger i Conductor)
    # if not Usuari.query.filter_by(nom_usuari="jordi").first():
    #     jordi = Usuari(
    #         nom_usuari="jordi",
    #         contrasenya=generate_password_hash("password123"),
    #         nom_complet="Jordi Serra",
    #         email="jordi@example.com",
    #         telefon_fix="977000111",
    #         telefon_mobil="666123456",
    #         adreca="Carrer Major, Tortosa",
    #         ubicacio=ubicacions["Tortosa centre"],
    #         data_naixement=datetime(1985, 4, 12),
    #         avatar=None
    #     )
    #     db.session.add(jordi)
    #     db.session.commit()
    #
    #     passatger_jordi = Passatger(
    #         usuari_id=jordi.id,
    #         vegades_impuntuals=0,
    #         vegades_no_presentat=0,
    #         necessita_seient_davanter=False
    #     )
    #     db.session.add(passatger_jordi)
    #     db.session.commit()
    #
    #     conductor_jordi = Conductor(
    #         usuari_id=jordi.id,
    #         carnet_categoria_superior="B",
    #         accidents_tinguts=1
    #     )
    #     db.session.add(conductor_jordi)
    #     db.session.commit()
    #
    #     vehicle_jordi = Vehicle(
    #         matricula="1234XYZ",
    #         marca="Ford",
    #         model="Focus",
    #         color="Blau",
    #         num_places=5,
    #         tipus_vehicle=tipus_vehicles["Cotxe"]
    #     )
    #     db.session.add(vehicle_jordi)
    #     db.session.commit()
    #
    #     # Assignar vehicle a conductor
    #     conductor_jordi.vehicles.append(vehicle_jordi)
    #     db.session.commit()
    #
    # # Usuari: Maria (només Passatger)
    # if not Usuari.query.filter_by(nom_usuari="maria").first():
    #     maria = Usuari(
    #         nom_usuari="maria",
    #         contrasenya=generate_password_hash("pass456"),
    #         nom_complet="Maria Puig",
    #         email="maria@example.com",
    #         telefon_fix="977000222",
    #         telefon_mobil="666654321",
    #         adreca="Plaça Nova, Roquetes",
    #         ubicacio=ubicacions["Roquetes ciutat"],
    #         data_naixement=datetime(1990, 11, 5),
    #         avatar=None
    #     )
    #     db.session.add(maria)
    #     db.session.commit()
    #
    #     passatger_maria = Passatger(
    #         usuari_id=maria.id,
    #         vegades_impuntuals=0,
    #         vegades_no_presentat=0,
    #         necessita_seient_davanter=False
    #     )
    #     db.session.add(passatger_maria)
    #     db.session.commit()

    # Usuari: Admin (Passatger i Super Admin, no Conductor)
    if not Usuari.query.filter_by(nom_usuari="admin").first():
        admin = Usuari(
            nom_usuari="admin",
            contrasenya=generate_password_hash("LoPort1447"),
            nom_complet="Administrador General",
            email="admin@example.com",
            telefon_fix="000000000",
            telefon_mobil="000000000",
            adreca="Plaça de l'Ajuntament, Tortosa",
            ubicacio=ubicacions["Tortosa centre"],
            data_naixement=datetime(1980, 1, 1),
            avatar=None,
            super_admin=True
        )
        db.session.add(admin)
        db.session.commit()

        passatger_admin = Passatger(
            usuari_id=admin.id,
            vegades_impuntuals=0,
            vegades_no_presentat=0,
            necessita_seient_davanter=False
        )
        db.session.add(passatger_admin)
        db.session.commit()