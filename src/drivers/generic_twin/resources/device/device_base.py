import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_device import generic_twin_device_all_fields, \
    generic_twin_device_all_fields_with_children, generic_twin_device_all_attributes
from src.resources.utils import model_marshaller_with_children

from src.drivers.generic_twin.models.device import GenericTwinDeviceModel


def generic_twin_device_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, generic_twin_device_all_fields,
                                          generic_twin_device_all_fields_with_children)


class GenericTwinDeviceBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_twin_device_all_attributes:
        parser.add_argument(attr,
                            type=generic_twin_device_all_attributes[attr]['type'],
                            required=generic_twin_device_all_attributes[attr].get('required', False),
                            help=generic_twin_device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_device(cls, data):
        _uuid = str(uuid.uuid4())
        device = GenericTwinDeviceModel(uuid=_uuid, **data)
        device.save_to_db()
        return device
