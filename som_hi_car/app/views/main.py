from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from app.models import Viatge
from app.utils import admin_required, conductor_required, admin_or_conductor_required
from app.controllers.profile_controller import ProfileController
from app.controllers.viatge_controller import ViatgeController

bp_main = Blueprint('main', __name__)

@bp_main.route('/')
def home():
    # Fetch the trips (viatges)
    viatges = Viatge.query.filter_by(realitzat=False).order_by(Viatge.data_hora_inici.desc()).all()
    return render_template('home.html', viatges=viatges)


@bp_main.route('/viatges', methods=['GET'])
@login_required
@admin_or_conductor_required
def viatges():
    return ViatgeController.get_viatges(0)

@bp_main.route('/viatgesP', methods=['GET'])
@login_required
@admin_or_conductor_required
def viatges_pendents():
    return ViatgeController.get_viatges(1)

@bp_main.route('/viatgesR', methods=['GET'])
@login_required
@admin_or_conductor_required
def viatges_realitzats():
    return ViatgeController.get_viatges(2)

@bp_main.route('/viatges/nou', methods=['GET', 'POST'])
@login_required
@admin_or_conductor_required
def create_viatge():
    return ViatgeController.create_viatge()

@bp_main.route('/viatges/<int:viatge_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_or_conductor_required
def edit_viatge(viatge_id):
    return ViatgeController.edit_viatge(viatge_id)

@bp_main.route('/viatges/<int:viatge_id>/eliminar', methods=['POST'])
@login_required
@admin_or_conductor_required
def delete_viatge(viatge_id):
    return ViatgeController.delete_viatge(viatge_id)

@bp_main.route('/conductors', methods=['GET'])
@login_required
@admin_required
def conductors():
    from app.controllers.conductor_controller import ConductorController
    return ConductorController.get_conductors()

@bp_main.route('/conductors/nou', methods=['GET', 'POST'])
@login_required
@admin_required
def create_conductor():
    from app.controllers.conductor_controller import ConductorController
    return ConductorController.create_conductor()

@bp_main.route('/conductors/<int:conductor_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_conductor(conductor_id):
    from app.controllers.conductor_controller import ConductorController
    return ConductorController.edit_conductor(conductor_id)

@bp_main.route('/conductors/<int:conductor_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_conductor(conductor_id):
    from app.controllers.conductor_controller import ConductorController
    return ConductorController.delete_conductor()

@bp_main.route('/vehicles', methods=['GET'])
@login_required
@admin_required
def vehicles():
    from app.controllers.vehicle_controller import VehicleController
    return VehicleController.get_vehicles()

@bp_main.route('/vehicles/nou', methods=['GET', 'POST'])
@login_required
@admin_required
def create_vehicle():
    from app.controllers.vehicle_controller import VehicleController
    return VehicleController.create_vehicle()

@bp_main.route('/vehicles/nou_user', methods=['GET', 'POST'])
@login_required
def create_vehicle_user():
    return ProfileController.create_vehicle()

@bp_main.route('/vehicles/<int:vehicle_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_vehicle(vehicle_id):
    from app.controllers.vehicle_controller import VehicleController
    return VehicleController.edit_vehicle(vehicle_id)

@bp_main.route('/vehicles/<int:vehicle_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_vehicle(vehicle_id):
    from app.controllers.vehicle_controller import VehicleController
    return VehicleController.delete_vehicle(vehicle_id)

@bp_main.route('/tipus_vehicles', methods=['GET'])
@login_required
@admin_required
def tipus_vehicles():
    from app.controllers.tipus_vehicle_controller import TipusVehicleController
    return TipusVehicleController.get_tipus_vehicles()

@bp_main.route('/tipus_vehicles/nou', methods=['GET', 'POST'])
@login_required
@admin_required
def create_tipus_vehicle():
    from app.controllers.tipus_vehicle_controller import TipusVehicleController
    return TipusVehicleController.create_tipus_vehicle()

@bp_main.route('/tipus_vehicles/<int:tipus_vehicle_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tipus_vehicle(tipus_vehicle_id):
    from app.controllers.tipus_vehicle_controller import TipusVehicleController
    return TipusVehicleController.edit_tipus_vehicle(tipus_vehicle_id)

@bp_main.route('/tipus_vehicles/<int:tipus_vehicle_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_tipus_vehicle(tipus_vehicle_id):
    from app.controllers.tipus_vehicle_controller import TipusVehicleController
    return TipusVehicleController.delete_tipus_vehicle(tipus_vehicle_id)

@bp_main.route('/ubicacions', methods=['GET'])
@login_required
@admin_required
def ubicacions():
    from app.controllers.ubicacio_controller import UbicacioController
    return UbicacioController.get_ubicacions()

@bp_main.route('/ubicacions/nou', methods=['GET', 'POST'])
@login_required
@admin_required
def create_ubicacio():
    from app.controllers.ubicacio_controller import UbicacioController
    return UbicacioController.create_ubicacio()

@bp_main.route('/ubicacions/<int:ubicacio_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_ubicacio(ubicacio_id):
    from app.controllers.ubicacio_controller import UbicacioController
    return UbicacioController.edit_ubicacio(ubicacio_id)

@bp_main.route('/ubicacions/<int:ubicacio_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_ubicacio(ubicacio_id):
    from app.controllers.ubicacio_controller import UbicacioController
    return UbicacioController.delete_ubicacio(ubicacio_id)

@bp_main.route('/sectors', methods=['GET'])
@login_required
@admin_required
def sectors():
    from app.controllers.sector_controller import SectorController
    return SectorController.get_sectors()

@bp_main.route('/sectors/nou', methods=['GET', 'POST'])
@login_required
@admin_required
def create_sector():
    from app.controllers.sector_controller import SectorController
    return SectorController.create_sector()

@bp_main.route('/sectors/<int:sector_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_sector(sector_id):
    from app.controllers.sector_controller import SectorController
    return SectorController.edit_sector(sector_id)

@bp_main.route('/sectors/<int:sector_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_sector(sector_id):
    from app.controllers.sector_controller import SectorController
    return SectorController.delete_sector(sector_id)

@bp_main.route('/reserves', methods=['GET'])
@login_required
def reserves():
    from app.controllers.reserva_controller import ReservaController
    return ReservaController.get_reserves()

@bp_main.route('/viatges/<int:viatge_id>/reserves/lista', methods=['GET', 'POST'])
@login_required
@admin_or_conductor_required
def reserves_viatge(viatge_id):
    from app.controllers.reserva_controller import ReservaController
    return ReservaController.get_reserves_viatge(viatge_id)


@bp_main.route('/viatges/<int:viatge_id>/reserves/nou', methods=['GET', 'POST'])
def create_reserva(viatge_id):
    if not current_user.is_authenticated:
        flash("Has d'iniciar sessió per accedir a aquesta funcionalitat.", "warning")
        return redirect(url_for('auth.login'))
    from app.controllers.reserva_controller import ReservaController
    return ReservaController.create_reserva(viatge_id)

@bp_main.route('/reserves/<int:reserva_id>/<int:conductor>/editar', methods=['GET', 'POST'])
def edit_reserva(reserva_id, conductor):
    from app.controllers.reserva_controller import ReservaController
    return ReservaController.edit_reserva(reserva_id,conductor)


@bp_main.route('/reserves/<int:reserva_id>/<int:conductor>/eliminar', methods=['POST'])
def delete_reserva(reserva_id,conductor):
    from app.controllers.reserva_controller import ReservaController
    return ReservaController.delete_reserva(reserva_id, conductor)

@bp_main.route('/reserves/<int:reserva_id>/confirmar', methods=['POST'])
def confirma_reserva(reserva_id):
    from app.controllers.reserva_controller import ReservaController
    return ReservaController.confirma_reserva(reserva_id)

@bp_main.route('/reserves/<int:reserva_id>/eliminar_viatge', methods=['POST'])
def delete_reserva_viatge(reserva_id):
    from app.controllers.reserva_controller import ReservaController
    return ReservaController.delete_reserva_viatge(reserva_id)

@bp_main.route('/parades', methods=['GET'])
@login_required
@admin_required
def parades():
    from app.controllers.parada_controller import ParadaController
    return ParadaController.get_parades()

@bp_main.route('/parades/nou', methods=['GET', 'POST'])
@login_required
@admin_required
def create_parada():
    from app.controllers.parada_controller import ParadaController
    return ParadaController.create_parada()

@bp_main.route('/parades/<int:parada_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_parada(parada_id):
    from app.controllers.parada_controller import ParadaController
    return ParadaController.edit_parada(parada_id)

@bp_main.route('/parades/<int:parada_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_parada(parada_id):
    from app.controllers.parada_controller import ParadaController
    return ParadaController.delete_parada(parada_id)

@bp_main.route('/passatgers', methods=['GET'])
@login_required
@admin_required
def passatgers():
    from app.controllers.passatger_controller import PassatgerController
    return PassatgerController.get_passatgers()

@bp_main.route('/passatgers/nou', methods=['GET', 'POST'])
@login_required
@admin_required
def create_passatger():
    from app.controllers.passatger_controller import PassatgerController
    return PassatgerController.create_passatger()

@bp_main.route('/passatgers/<int:passatger_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_passatger(passatger_id):
    from app.controllers.passatger_controller import PassatgerController
    return PassatgerController.edit_passatger(passatger_id)

@bp_main.route('/passatgers/<int:passatger_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_passatger(passatger_id):
    from app.controllers.passatger_controller import PassatgerController
    return PassatgerController.delete_passatger(passatger_id)

@bp_main.route('/perfil')
@login_required
def perfil():
    return ProfileController.show_profile()

@bp_main.route('/perfil/actualitzar', methods=['POST'])
def update_profile():
    return ProfileController.update_profile()