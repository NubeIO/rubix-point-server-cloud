from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.generic_twin.models.point import GenericTwinPointModel
from src.drivers.generic_twin.resources.point.point_base import GenericTwinPointBase
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_point import generic_twin_point_all_attributes, \
    generic_twin_point_all_fields
from src.models.point.priority_array import PriorityArrayModel


class GenericTwinPointSingular(GenericTwinPointBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_twin_point_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_twin_point_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(generic_twin_point_all_fields)
    def get(cls, **kwargs):
        point: GenericTwinPointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Generic Twin Point not found')
        return point

    @classmethod
    @marshal_with(generic_twin_point_all_fields)
    def put(cls, **kwargs):
        data: dict = cls.parser.parse_args()
        point: GenericTwinPointModel = cls.get_point(**kwargs)
        if point is None:
            return cls.add_point(data)
        return cls.update_point(data, point)

    @classmethod
    def update_point(cls, data: dict, point: GenericTwinPointModel) -> GenericTwinPointModel:
        priority_array_write: dict = data.pop('priority_array_write') if data.get('priority_array_write') else {}
        if priority_array_write:
            PriorityArrayModel.filter_by_point_uuid(point.uuid).update(priority_array_write)
        updated_point: GenericTwinPointModel = point.update(**data)
        return updated_point

    @classmethod
    @marshal_with(generic_twin_point_all_fields)
    def patch(cls, **kwargs):
        data: dict = cls.patch_parser.parse_args()
        point: GenericTwinPointModel = cls.get_point(**kwargs)
        if point is None:
            raise NotFoundException('Generic Twin Point not found')
        return cls.update_point(data, point)

    @classmethod
    def delete(cls, **kwargs):
        point: GenericTwinPointModel = cls.get_point(**kwargs)
        if point is None:
            raise NotFoundException('Generic Twin Point not found')
        point.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericTwinPointModel:
        raise NotImplementedError


class GenericTwinPointSingularByUUID(GenericTwinPointSingular):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericTwinPointModel:
        return GenericTwinPointModel.find_by_uuid(kwargs.get('uuid'))


class GenericTwinPointSingularByName(GenericTwinPointSingular):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericTwinPointModel:
        return GenericTwinPointModel.find_by_name(kwargs.get('network_master_name'), kwargs.get('network_name'),
                                                  kwargs.get('device_name'), kwargs.get('point_name'))
