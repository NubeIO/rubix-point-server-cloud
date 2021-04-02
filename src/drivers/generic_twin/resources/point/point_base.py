import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic_twin.models.point import GenericTwinPointModel
from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_point import generic_twin_point_all_attributes, \
    add_nested_priority_array_write
from src.models.point.priority_array import PriorityArrayModel


class GenericTwinPointBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_twin_point_all_attributes:
        parser.add_argument(attr,
                            type=generic_twin_point_all_attributes[attr]['type'],
                            required=generic_twin_point_all_attributes[attr].get('required', False),
                            help=generic_twin_point_all_attributes[attr].get('help', None),
                            store_missing=False)
    add_nested_priority_array_write()

    @classmethod
    def add_point(cls, data):
        _uuid: str = str(uuid.uuid4())
        priority_array_write: dict = data.pop('priority_array_write', {})
        point = GenericTwinPointModel(
            uuid=_uuid,
            priority_array_write=PriorityArrayModel.create_priority_array_model(_uuid, priority_array_write),
            **data
        )
        point.save_to_db()
        return point
