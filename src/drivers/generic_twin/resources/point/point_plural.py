from flask_restful import marshal_with

from src.drivers.generic_twin.models.point import GenericTwinPointModel
from src.drivers.generic_twin.resources.point.point_base import GenericTwinPointBase
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_point import generic_twin_point_all_fields


class GenericTwinPointPlural(GenericTwinPointBase):
    @classmethod
    @marshal_with(generic_twin_point_all_fields)
    def get(cls):
        points = GenericTwinPointModel.find_all()
        return points

    @classmethod
    @marshal_with(generic_twin_point_all_fields)
    def post(cls):
        data = GenericTwinPointPlural.parser.parse_args()
        return cls.add_point(data)
