from src.drivers.generic_twin.resources.rest_schema.schema_generic_twin_network import \
    generic_twin_network_all_fields_with_children
from src.resources.rest_schema.schema_network import *

generic_twin_network_master_all_attributes = {
    'name': {
        'type': str,
        'required': True,
    },
    'type': {
        'type': str,
        'nested': True,
        'required': True,
        'dict': 'type.name'
    }
}
generic_twin_network_master_return_attributes = {
    'uuid': {
        'type': str,
    },
}

generic_twin_network_master_all_fields = {}
map_rest_schema(generic_twin_network_master_all_attributes, generic_twin_network_master_all_fields)
map_rest_schema(generic_twin_network_master_return_attributes, generic_twin_network_master_all_fields)

generic_twin_network_master_all_fields_with_children = deepcopy(generic_twin_network_master_all_fields)
generic_twin_network_master_all_fields_with_children['networks'] = fields.List(
    fields.Nested(generic_twin_network_all_fields_with_children))