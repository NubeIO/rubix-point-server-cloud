from copy import deepcopy

from src.resources.rest_schema.schema_point import point_return_attributes, point_all_attributes
from src.resources.utils import map_rest_schema

generic_twin_point_all_attributes = deepcopy(point_all_attributes)
generic_twin_point_all_attributes['type'] = {
    'type': str,
    'nested': True,
    'dict': 'type.name'
}
generic_twin_point_all_attributes['unit'] = {
    'type': str,
}

generic_twin_point_return_attributes = deepcopy(point_return_attributes)
generic_twin_point_all_fields = {}
map_rest_schema(generic_twin_point_all_attributes, generic_twin_point_all_fields)
map_rest_schema(generic_twin_point_return_attributes, generic_twin_point_all_fields)
