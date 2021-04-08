from flask import Blueprint
from flask_restful import Api

from src.discover.resources.remote_device import RemoteDevice
from src.drivers.generic_twin.resources.device.device_plural import GenericTwinDevicePlural
from src.drivers.generic_twin.resources.device.device_singular import GenericTwinDeviceSingularByUUID, \
    GenericTwinDeviceSingularByName
from src.drivers.generic_twin.resources.network.network_plural import GenericTwinNetworkPlural
from src.drivers.generic_twin.resources.network.network_singular import GenericNetworkSingularByUUID, \
    GenericNetworkSingularByName
from src.drivers.generic_twin.resources.network_master.network_master_plural import GenericTwinNetworkMasterPlural
from src.drivers.generic_twin.resources.network_master.network_master_singular import \
    GenericTwinNetworkMasterSingularByUUID, GenericTwinNetworkMasterSingularByName
from src.drivers.generic_twin.resources.point.point_plural import GenericTwinPointPlural
from src.drivers.generic_twin.resources.point.point_singular import GenericTwinPointSingularByUUID, \
    GenericTwinPointSingularByName

from src.system.resources.ping import Ping

bp_generic_twin = Blueprint('generic_twin', __name__, url_prefix='/api/generic_twin')
api_generic_twin = Api(bp_generic_twin)
api_generic_twin.add_resource(GenericTwinNetworkMasterPlural, '/networks_masters')
api_generic_twin.add_resource(GenericTwinNetworkMasterSingularByUUID, '/networks_masters/uuid/<string:uuid>')
api_generic_twin.add_resource(GenericTwinNetworkMasterSingularByName, '/networks_masters/name/<string:name>')
api_generic_twin.add_resource(GenericTwinNetworkPlural, '/networks')
api_generic_twin.add_resource(GenericNetworkSingularByUUID, '/networks/uuid/<string:uuid>')
api_generic_twin.add_resource(GenericNetworkSingularByName,
                              '/networks/name/<string:network_master_name>/<string:network_name>')
api_generic_twin.add_resource(GenericTwinDevicePlural, '/devices')
api_generic_twin.add_resource(GenericTwinDeviceSingularByUUID, '/devices/uuid/<string:uuid>')
api_generic_twin.add_resource(GenericTwinDeviceSingularByName,
                              '/devices/name/<string:network_master_name>/<string:network_name>/<string:device_name>')
api_generic_twin.add_resource(GenericTwinPointPlural, '/points')
api_generic_twin.add_resource(GenericTwinPointSingularByUUID, '/points/uuid/<string:uuid>')
api_generic_twin.add_resource(GenericTwinPointSingularByName,
                              '/points/name/<string:network_master_name>/<string:network_name>/<string:device_name>/'
                              '<string:point_name>')

bp_discover = Blueprint('discover', __name__, url_prefix='/api/discover')
api_discover = Api(bp_discover)
api_discover.add_resource(RemoteDevice, '/remote_devices')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
