from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_device import \
    generic_twin_device_all_fields_with_children, generic_twin_device_all_fields
from src.resources.rest_schema.schema_network import *

generic_twin_network_all_attributes = {
    **deepcopy(network_all_attributes),
    'network_master_uuid': {
        'type': str,
        'required': True,
    },
}
generic_twin_network_return_attributes = deepcopy(network_return_attributes)

generic_twin_network_all_fields = {}
map_rest_schema(generic_twin_network_all_attributes, generic_twin_network_all_fields)
map_rest_schema(generic_twin_network_return_attributes, generic_twin_network_all_fields)

generic_twin_network_all_fields_with_children = deepcopy(generic_twin_network_all_fields)
generic_twin_network_all_fields_with_children['devices'] = fields.List(fields.Nested(
    generic_twin_device_all_fields_with_children))

generic_twin_network_all_fields_without_point_children = deepcopy(generic_twin_network_all_fields)
generic_twin_network_all_fields_without_point_children['devices'] = fields.List(
    fields.Nested(generic_twin_device_all_fields))
