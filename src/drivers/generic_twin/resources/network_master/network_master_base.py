import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic_twin.models.network_master import GenericTwinNetworkMasterModel
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_network_master import \
    generic_twin_network_master_all_fields, generic_twin_network_master_all_fields_with_children, \
    generic_twin_network_master_all_attributes
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
        _uuid = str(uuid.uuid4())
        network_master: GenericTwinNetworkMasterModel = GenericTwinNetworkMasterModel(uuid=_uuid, **data)
        network_master.save_to_db()
        return network_master
