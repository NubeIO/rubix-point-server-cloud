import logging
from threading import Thread

import gevent
from flask import current_app

from .setting import AppSetting

logger = logging.getLogger(__name__)


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


class Background:

    @staticmethod
    def run():
        setting: AppSetting = current_app.config[AppSetting.KEY]

        # Services
        logger.info("Starting Services...")
        from src.discover.remote_device_registry import RemoteDeviceRegistry
        gevent.spawn(RemoteDeviceRegistry().register)

        if setting.services.mqtt:
            from src.services.mqtt_client import MqttClient
            for config in setting.mqtt_settings:
                if not config.enabled:
                    continue
                mqtt_client = MqttClient()
                FlaskThread(target=mqtt_client.start, daemon=True, kwargs={'config': config}).start()

        if setting.services.histories:
            from src.services.histories.history_local import HistoryLocal
            FlaskThread(target=HistoryLocal().sync_interval, daemon=True).start()

        if setting.services.cleaner:
            from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner
            FlaskThread(target=PointStoreHistoryCleaner().setup, daemon=True,
                        kwargs={'config': setting.cleaner}).start()

        if setting.services.history_sync_influxdb:
            from src.services.histories.sync.influxdb import InfluxDB
            FlaskThread(target=InfluxDB().setup, daemon=True,
                        kwargs={'config': setting.influx}).start()

        if setting.services.history_sync_postgres:
            from src.services.histories.sync.postgresql import PostgreSQL
            FlaskThread(target=PostgreSQL().setup, daemon=True,
                        kwargs={'config': setting.postgres}).start()
