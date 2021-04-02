import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic_twin.models.network import GenericTwinNetworkModel
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_network import generic_twin_network_all_fields, \
    generic_twin_network_all_fields_without_point_children, generic_twin_network_all_fields_with_children, \
    generic_twin_network_all_attributes
from src.resources.utils import model_network_marshaller


def generic_twin_network_marshaller(data: any, args: dict):
    return model_network_marshaller(data, args, generic_twin_network_all_fields,
                                    generic_twin_network_all_fields_without_point_children,
                                    generic_twin_network_all_fields_with_children)


class GenericTwinNetworkBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_twin_network_all_attributes:
        parser.add_argument(attr,
                            type=generic_twin_network_all_attributes[attr].get('type'),
                            required=generic_twin_network_all_attributes[attr].get('required', False),
                            help=generic_twin_network_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def add_network(data):
        _uuid = str(uuid.uuid4())
        network: GenericTwinNetworkModel = GenericTwinNetworkModel(uuid=_uuid, **data)
        network.save_to_db()
        return network
