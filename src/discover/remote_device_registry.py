import json
import logging
from typing import List, Dict

from rubix_http.request import gw_mqtt_slaves_broadcast_request

from src.drivers.generic_twin.models.network_master import GenericTwinNetworkMasterModel
from src.utils import Singleton

logger = logging.getLogger(__name__)


class RemoteDeviceRegistry(metaclass=Singleton):
    def __init__(self):
        self.app_context = None
        self.__devices: List[Dict[str, str]] = []
        self.__devices_global_uuids: List[str] = []
        self.__registered_available_devices_global_uuids: List[str] = []

    @property
    def devices(self) -> List[Dict[str, str]]:
        return self.__devices

    @property
    def devices_global_uuids(self) -> List[str]:
        return self.__devices_global_uuids

    @property
    def registered_available_devices_global_uuids(self) -> List[str]:
        return self.__registered_available_devices_global_uuids

    def register(self, app_context):
        logger.info(f"Called devices registration")
        self.app_context = app_context
        while True:
            self.poll_devices()

    def poll_devices(self):
        """
        We don't need to sleep the response itself has sleep of bridge timeout seconds
        """
        devices: dict = json.loads(gw_mqtt_slaves_broadcast_request('/api/wires/plat').data)
        temp_devices: List[Dict[str, str]] = []
        temp_devices_global_uuids: List[str] = []
        temp_registered_available_devices_global_uuids: List[str] = []
        for device in devices:
            temp_devices.append(devices[device])
            temp_devices_global_uuids.append(device)
        with self.app_context():
            for network_master in GenericTwinNetworkMasterModel.find_all():
                if network_master.global_uuid in temp_devices_global_uuids:
                    temp_registered_available_devices_global_uuids.append(network_master.global_uuid)
        self.__devices = temp_devices
        self.__devices_global_uuids = temp_devices_global_uuids
        self.__registered_available_devices_global_uuids = temp_registered_available_devices_global_uuids
