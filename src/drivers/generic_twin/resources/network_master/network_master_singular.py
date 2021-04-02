from abc import abstractmethod

from flask_restful import reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.generic_twin.models.network_master import GenericTwinNetworkMasterModel
from src.drivers.generic_twin.resources.network.network_base import generic_twin_network_marshaller
from src.drivers.generic_twin.resources.network_master.network_master_base import GenericTwinNetworkMasterBase, \
    generic_twin_network_master_marshaller
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_network_master import \
    generic_twin_network_master_all_attributes


class GenericTwinNetworkMasterSingular(GenericTwinNetworkMasterBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_twin_network_master_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_twin_network_master_all_attributes[attr].get('type'),
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        network_master: GenericTwinNetworkMasterModel = cls.get_network_master(**kwargs)
        if not network_master:
            raise NotFoundException('Generic Twin Network not found')
        return generic_twin_network_master_marshaller(network_master, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        network_master: GenericTwinNetworkMasterModel = cls.get_network_master(**kwargs)
        if network_master is None:
            return generic_twin_network_marshaller(cls.add_network_master(data), request.args)
        network_master.update(**data)
        return generic_twin_network_marshaller(cls.get_network_master(**{**kwargs, **data}), request.args)

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        network_master: GenericTwinNetworkMasterModel = cls.get_network_master(**kwargs)
        if network_master is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network_master.update(**data)
        return generic_twin_network_marshaller(cls.get_network_master(**{**kwargs, **data}), request.args)

    @classmethod
    def delete(cls, **kwargs):
        network_master: GenericTwinNetworkMasterModel = cls.get_network_master(**kwargs)
        if network_master is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network_master.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_network_master(cls, **kwargs) -> GenericTwinNetworkMasterModel:
        raise NotImplementedError


class GenericTwinNetworkMasterSingularByUUID(GenericTwinNetworkMasterSingular):
    @classmethod
    def get_network_master(cls, **kwargs) -> GenericTwinNetworkMasterModel:
        return GenericTwinNetworkMasterModel.find_by_uuid(kwargs.get('uuid'))


class GenericTwinNetworkMasterSingularByName(GenericTwinNetworkMasterSingular):
    @classmethod
    def get_network_master(cls, **kwargs) -> GenericTwinNetworkMasterModel:
        return GenericTwinNetworkMasterModel.find_by_name(kwargs.get('name'))
