from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from database.db import db  # Importem db des de database/db.py
from flask_login import UserMixin

# Taula d'associació per a conductors i vehicles (molts a molts)
conductors_vehicles = Table(
    'conductors_vehicles',
    db.Model.metadata,
    Column('conductor_id', Integer, ForeignKey('conductors.id'), primary_key=True),
    Column('vehicle_id', Integer, ForeignKey('vehicles.id'), primary_key=True)
)

# Seqüències per a IDs (Oracle)
sector_id_seq = Sequence('sector_id_seq')
ubicacio_id_seq = Sequence('ubicacio_id_seq')
parada_id_seq = Sequence('parada_id_seq')
usuari_id_seq = Sequence('usuari_id_seq')
conductor_id_seq = Sequence('conductor_id_seq')
passatger_id_seq = Sequence('passatger_id_seq')
vehicle_id_seq = Sequence('vehicle_id_seq')
tipus_vehicle_id_seq = Sequence('tipus_vehicle_id_seq')
viatge_id_seq = Sequence('viatge_id_seq')
reserva_id_seq = Sequence('reserva_id_seq')

# Models
class Sector(db.Model):
    __tablename__ = 'sectors'
    id = Column(Integer, sector_id_seq, primary_key=True, server_default=sector_id_seq.next_value())
    descripcio = Column(String(255))
    es_port = Column(Boolean, default=False)
    ubicacions = relationship("Ubicacio", back_populates="sector")

class Ubicacio(db.Model):
    __tablename__ = 'ubicacions'
    id = Column(Integer, ubicacio_id_seq, primary_key=True, server_default=ubicacio_id_seq.next_value())
    nom = Column(String(100))
    sector_id = Column(Integer, ForeignKey('sectors.id'))
    sector = relationship("Sector", back_populates="ubicacions")
    parades = relationship("Parada", back_populates="ubicacio")

class Parada(db.Model):
    __tablename__ = 'parades'
    id = Column(Integer, parada_id_seq, primary_key=True, server_default=parada_id_seq.next_value())
    descripcio = Column(String(255))
    ubicacio_id = Column(Integer, ForeignKey('ubicacions.id'))
    separacio_port = Column(Integer)
    ubicacio = relationship("Ubicacio", back_populates="parades")


class Usuari(db.Model, UserMixin):
    __tablename__ = 'usuaris'
    id = Column(Integer, usuari_id_seq, primary_key=True, server_default=usuari_id_seq.next_value())
    nom_usuari = Column(String(150), unique=True, nullable=False)
    contrasenya = Column(String(255), nullable=False)
    nom_complet = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefon_fix = Column(String(15))
    telefon_mobil = Column(String(15))
    adreca = Column(String(500))
    ubicacio_id = Column(Integer, ForeignKey('ubicacions.id'))
    data_naixement = Column(DateTime)
    avatar = Column(String(255))
    super_admin = db.Column(db.Boolean, default=False, nullable=False)

    conductor = relationship("Conductor", uselist=False, back_populates="usuari", lazy='joined')
    passatger = relationship("Passatger", uselist=False, back_populates="usuari", lazy='joined')
    ubicacio = relationship("Ubicacio", lazy='joined')

class Conductor(db.Model):
    __tablename__ = 'conductors'
    id = Column(Integer, conductor_id_seq, primary_key=True, server_default=conductor_id_seq.next_value())
    usuari_id = Column(Integer, ForeignKey('usuaris.id'), unique=True)
    carnet_categoria_superior = Column(String(255))
    accidents_tinguts = Column(Integer, default=0)
    usuari = relationship("Usuari", back_populates="conductor")
    vehicles = relationship("Vehicle", secondary=conductors_vehicles, back_populates="conductors")

class Passatger(db.Model):
    __tablename__ = 'passatgers'
    id = Column(Integer, passatger_id_seq, primary_key=True, server_default=passatger_id_seq.next_value())
    usuari_id = Column(Integer, ForeignKey('usuaris.id'), unique=True)
    vegades_impuntuals = Column(Integer, default=0)
    vegades_no_presentat = Column(Integer, default=0)
    necessita_seient_davanter = Column(Boolean, default=False)
    usuari = relationship("Usuari", back_populates="passatger")


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = Column(Integer, vehicle_id_seq, primary_key=True, server_default=vehicle_id_seq.next_value())
    matricula = Column(String(20), unique=True, nullable=False)
    marca = Column(String(50))
    model = Column(String(50))
    color = Column(String(30))
    num_places = Column(Integer)
    tipus_vehicle_id = Column(Integer, ForeignKey('tipus_vehicles.id'))

    tipus_vehicle = relationship("TipusVehicle")
    conductors = relationship("Conductor", secondary=conductors_vehicles, back_populates="vehicles")

class TipusVehicle(db.Model):
    __tablename__ = 'tipus_vehicles'
    id = Column(Integer, tipus_vehicle_id_seq, primary_key=True, server_default=tipus_vehicle_id_seq.next_value())
    nom = Column(String(50), unique=True)

class Viatge(db.Model):
    __tablename__ = 'viatges'
    id = Column(Integer, viatge_id_seq, primary_key=True, server_default=viatge_id_seq.next_value())
    data_hora_inici = Column(DateTime, nullable=False)
    places_inicials = Column(Integer, nullable=False)
    places_restants = Column(Integer, nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    conductor_id = Column(Integer, ForeignKey('conductors.id'))
    parada_recollida_id = Column(Integer, ForeignKey('parades.id'), nullable=False)
    parada_arribada_id = Column(Integer, ForeignKey('parades.id'), nullable=False)
    sentit = Column(String(10))  # "muntada" or "baixada"
    confirmat = Column(Boolean, default=False)
    realitzat = Column(Boolean, default=False)
    import_ = Column(Float, default=0.0)
    observacions = Column(String(500))

    vehicle = relationship("Vehicle")
    conductor = relationship("Conductor")
    parada_recollida = relationship("Parada", foreign_keys=[parada_recollida_id])
    parada_arribada = relationship("Parada", foreign_keys=[parada_arribada_id])
    reserves = relationship("Reserva", back_populates="viatge")

class Reserva(db.Model):
    __tablename__ = 'reserves'
    id = Column(Integer, reserva_id_seq, primary_key=True, server_default=reserva_id_seq.next_value())
    viatge_id = Column(Integer, ForeignKey('viatges.id'))
    passatger_id = Column(Integer, ForeignKey('passatgers.id'))
    data_hora_realitzacio = Column(DateTime, nullable=False)
    parada_recollida_id = Column(Integer, ForeignKey('parades.id'))
    hora_estimada_recollida = Column(DateTime)
    parada_arribada_id = Column(Integer, ForeignKey('parades.id'))
    confirmada_passatger = Column(Boolean, default=False)
    confirmada_conductor = Column(Boolean, default=False)
    viatge = relationship("Viatge", back_populates="reserves")
    passatger = relationship("Passatger")
    parada_recollida = relationship("Parada", foreign_keys=[parada_recollida_id])
    parada_arribada = relationship("Parada", foreign_keys=[parada_arribada_id])