from flask_restful.reqparse import request

from src.drivers.generic_twin.models.device import GenericTwinDeviceModel
from src.drivers.generic_twin.resources.device.device_base import GenericTwinDeviceBase, generic_twin_device_marshaller


class GenericTwinDevicePlural(GenericTwinDeviceBase):

    @classmethod
    def get(cls):
        return generic_twin_device_marshaller(GenericTwinDeviceModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = GenericTwinDevicePlural.parser.parse_args()
        return generic_twin_device_marshaller(cls.add_device(data), request.args)
