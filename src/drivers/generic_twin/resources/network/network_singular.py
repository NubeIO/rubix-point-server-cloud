from abc import abstractmethod

from flask_restful import reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.generic_twin.models.network import GenericTwinNetworkModel
from src.drivers.generic_twin.resources.network.network_base import generic_twin_network_marshaller, \
    GenericTwinNetworkBase
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_network import \
    generic_twin_network_all_attributes


class GenericTwinNetworkSingular(GenericTwinNetworkBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_twin_network_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_twin_network_all_attributes[attr].get('type'),
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        network: GenericTwinNetworkModel = cls.get_network(**kwargs)
        if not network:
            raise NotFoundException('Generic Twin Network not found')
        return generic_twin_network_marshaller(network, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        network: GenericTwinNetworkModel = cls.get_network(**kwargs)
        if network is None:
            return generic_twin_network_marshaller(cls.add_network(data), request.args)
        network.update(**data)
        return generic_twin_network_marshaller(cls.get_network(**{**kwargs, **data}), request.args)

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        network: GenericTwinNetworkModel = cls.get_network(**kwargs)
        if network is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network.update(**data)
        return generic_twin_network_marshaller(cls.get_network(**{**kwargs, **data}), request.args)

    @classmethod
    def delete(cls, **kwargs):
        network: GenericTwinNetworkModel = cls.get_network(**kwargs)
        if network is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_network(cls, **kwargs) -> GenericTwinNetworkModel:
        raise NotImplementedError


class GenericNetworkSingularByUUID(GenericTwinNetworkSingular):
    @classmethod
    def get_network(cls, **kwargs) -> GenericTwinNetworkModel:
        return GenericTwinNetworkModel.find_by_uuid(kwargs.get('uuid'))


class GenericNetworkSingularByName(GenericTwinNetworkSingular):
    @classmethod
    def get_network(cls, **kwargs) -> GenericTwinNetworkModel:
        return GenericTwinNetworkModel.find_by_name(kwargs.get('network_master_name'), kwargs.get('network_name'))
