from abc import abstractmethod

from flask_restful import reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.generic_twin.models.device import GenericTwinDeviceModel
from src.drivers.generic_twin.resources.device.device_base import GenericTwinDeviceBase, generic_twin_device_marshaller
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_device import generic_twin_device_all_attributes


class GenericTwinDeviceSingular(GenericTwinDeviceBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_twin_device_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_twin_device_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        device: GenericTwinDeviceModel = cls.get_device(**kwargs)
        if not device:
            raise NotFoundException('Generic Twin Device not found')
        return generic_twin_device_marshaller(device, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        device: GenericTwinDeviceModel = cls.get_device(**kwargs)
        if device is None:
            return generic_twin_device_marshaller(cls.add_device(data), request.args)
        device.update(**data)
        return generic_twin_device_marshaller(cls.get_device(**kwargs), request.args)

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        device: GenericTwinDeviceModel = cls.get_device(**kwargs)
        if device is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        device.update(**data)
        return generic_twin_device_marshaller(cls.get_device(**kwargs), request.args)

    @classmethod
    def delete(cls, **kwargs):
        device: GenericTwinDeviceModel = cls.get_device(**kwargs)
        if device is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        device.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_device(cls, **kwargs) -> GenericTwinDeviceModel:
        raise NotImplementedError


class GenericTwinDeviceSingularByUUID(GenericTwinDeviceSingular):
    @classmethod
    def get_device(cls, **kwargs) -> GenericTwinDeviceModel:
        return GenericTwinDeviceModel.find_by_uuid(kwargs.get('uuid'))


class GenericTwinDeviceSingularByName(GenericTwinDeviceSingular):
    @classmethod
    def get_device(cls, **kwargs) -> GenericTwinDeviceModel:
        return GenericTwinDeviceModel.find_by_name(kwargs.get('network_master_name'), kwargs.get('network_name'),
                                                   kwargs.get('device_name'))
