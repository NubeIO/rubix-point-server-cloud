import uuid
from typing import List, Dict, Union

from flask_restful import reqparse
from rubix_http.exceptions.exception import BadDataException
from rubix_http.resource import RubixResource

from src.discover.remote_device_registry import RemoteDeviceRegistry
from src.drivers.generic_twin.models.network_master import GenericTwinNetworkMasterModel
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_network_master import \
    generic_twin_network_master_all_fields, generic_twin_network_master_all_fields_with_children, \
    generic_twin_network_master_all_attributes
from src.enums.network_master_type import NetworkMasterType
from src.resources.utils import model_marshaller_with_children


def generic_twin_network_master_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, generic_twin_network_master_all_fields,
                                          generic_twin_network_master_all_fields_with_children)


class GenericTwinNetworkMasterBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_twin_network_master_all_attributes:
        parser.add_argument(attr,
                            type=generic_twin_network_master_all_attributes[attr].get('type'),
                            required=generic_twin_network_master_all_attributes[attr].get('required', False),
                            help=generic_twin_network_master_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def add_network_master(data) -> GenericTwinNetworkMasterModel:
        if data.type == NetworkMasterType.INTEGRATION.name:
            data = {**data, 'global_uuid': str(uuid.uuid4())}
        else:
            devices: List[Dict[str, str]] = RemoteDeviceRegistry().devices
            global_uuid: str = data.get('global_uuid', '')
            if not global_uuid:
                raise BadDataException("global_uuid should be in your input")
            device: Union[Dict[str, str], None] = next(
                (device for device in devices if device.get('global_uuid') == global_uuid), None)
            if not device:
                raise BadDataException("Not found that global_uuid")
            del device['created_on']
            del device['updated_on']
            data = {**data, **device}
        network_master: GenericTwinNetworkMasterModel = GenericTwinNetworkMasterModel(**data)
        network_master.save_to_db()
        return network_master
