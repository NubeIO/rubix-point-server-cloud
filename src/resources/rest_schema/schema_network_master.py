network_master_all_attributes = {
    'global_uuid': {
        'type': str,
    },
    'name': {
        'type': str,
        'required': True,
    },
    'type': {
        'type': str,
        'nested': True,
        'required': True,
        'dict': 'type.name'
    },
    'client_id': {
        'type': str,
    },
    'client_name': {
        'type': str,
    },
    'site_id': {
        'type': str,
    },
    'site_name': {
        'type': str,
    },
    'device_id': {
        'type': str,
    },
    'device_name': {
        'type': str,
    },
    'site_address': {
        'type': str,
    },
    'site_city': {
        'type': str,
    },
    'site_state': {
        'type': str,
    },
    'site_zip': {
        'type': str,
    },
    'site_country': {
        'type': str,
    },
    'site_lat': {
        'type': str,
    },
    'site_lon': {
        'type': str,
    },
}

network_master_return_attributes = {
    'driver': {
        'type': str,
        'nested': True,
        'dict': 'driver.name'
    },
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    }
}
