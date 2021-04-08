import json
import logging
from typing import List, Dict

from rubix_http.request import gw_mqtt_slaves_request

from src.utils import Singleton

logger = logging.getLogger(__name__)


class RemoteDeviceRegistry(metaclass=Singleton):
    def __init__(self):
        self.__devices: List[Dict[str, str]] = []

    @property
    def devices(self) -> List[Dict[str, str]]:
        return self.__devices

    def register(self):
        logger.info(f"Called devices registration")
        while True:
            self.poll_devices()

    def poll_devices(self):
        """
        We don't need to sleep the response itself has sleep of bridge timeout seconds
        """
        devices: dict = json.loads(gw_mqtt_slaves_request('/api/wires/plat').data)
        devices_temp: List[Dict[str, str]] = []
        for device in devices:
            devices_temp.append(devices[device])
        self.__devices = devices_temp
