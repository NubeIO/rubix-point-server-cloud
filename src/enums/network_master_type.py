import enum


class NetworkMasterType(enum.Enum):
    """
    INTEGRATION : it is created for those whose values will get sync from third party
    EDGE        : it is created for those whose values will be sync from the edge rubix_point_server (two way binding)
    """
    INTEGRATION = 'integration'
    EDGE = 'edge'
