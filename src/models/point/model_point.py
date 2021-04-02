import json
import logging
import re
from abc import abstractmethod

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.enums.model import ModelEvent
from src.enums.point import HistoryType, MathOperation
from src.models.device.model_device import DeviceModel
from src.models.model_base import ModelBase
from src.models.network.model_network import NetworkModel
from src.models.network_master.model_network_master import NetworkMasterModel
from src.models.point.model_point_store import PointStoreModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.models.point.priority_array import PriorityArrayModel
from src.services.event_service_base import Event, EventType

logger = logging.getLogger(__name__)


class PointModel(ModelBase):
    __tablename__ = 'points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    history_type = db.Column(db.Enum(HistoryType), nullable=False, default=HistoryType.INTERVAL)
    history_interval = db.Column(db.Integer, nullable=False, default=15)
    writable = db.Column(db.Boolean, nullable=False, default=False)
    priority_array_write = db.relationship('PriorityArrayModel',
                                           backref='points',
                                           lazy=False,
                                           uselist=False,
                                           cascade="all,delete")
    cov_threshold = db.Column(db.Float, nullable=False, default=0)
    value_round = db.Column(db.Integer(), nullable=False, default=2)
    value_offset = db.Column(db.Float(), nullable=False, default=0)
    value_operation = db.Column(db.Enum(MathOperation), nullable=True)
    input_min = db.Column(db.Float())
    input_max = db.Column(db.Float())
    scale_min = db.Column(db.Float())
    scale_max = db.Column(db.Float())
    tags = db.Column(db.String(320), nullable=True)
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")
    point_store_history = db.relationship('PointStoreHistoryModel', backref='point', lazy=False, cascade="all,delete")
    driver = db.Column(db.Enum(Drivers), default=Drivers.GENERIC)

    __mapper_args__ = {
        'polymorphic_identity': 'point',
        'polymorphic_on': driver
    }

    __table_args__ = (
        UniqueConstraint('name', 'device_uuid'),
    )

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

    @validates('name')
    def validate_name(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("name should be alphanumeric and can contain '_', '-'")
        return value

    @classmethod
    def find_by_name(cls, network_master_name: str, network_name: str, device_name: str, point_name: str):
        results = cls.query.filter_by(name=point_name) \
            .join(DeviceModel).filter_by(name=device_name) \
            .join(NetworkModel).filter_by(name=network_name) \
            .join(NetworkMasterModel).filter_by(name=network_master_name) \
            .first()
        return results

    def save_to_db(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        super().save_to_db()

    def update_point_value(self, point_store: PointStoreModel, driver: Drivers, cov_threshold: float = None) -> bool:
        if not point_store.fault:
            if cov_threshold is None:
                cov_threshold = self.cov_threshold

            value = point_store.value_original
            if value is not None:
                value = self.apply_scale(value, self.input_min, self.input_max, self.scale_min,
                                         self.scale_max)
                value = self.apply_offset(value, self.value_offset, self.value_operation)
                value = round(value, self.value_round)
            point_store.value = self.apply_point_type(value)
        return point_store.update(driver, cov_threshold)

    @validates('tags')
    def validate_tags(self, _, value):
        """
        Rules for tags:
        - force all tags to be lower case
        - if there is a gap add an underscore
        - no special characters
        """
        if value is not None:
            try:
                tags = json.loads(value)
                return_tags: dict = {}
                for tag in tags:
                    clean_tag: str = tag.lower()
                    clean_tag = clean_tag.replace(" ", "_")
                    clean_tag = re.sub('[^A-Za-z0-9_]+', '', clean_tag)
                    return_tags[clean_tag] = tags[tag]
                return json.dumps(return_tags)
            except ValueError:
                raise ValueError('tags needs to be a valid JSON')
        return value

    @validates('history_interval')
    def validate_history_interval(self, _, value):
        if self.history_type == HistoryType.INTERVAL and value is not None and value < 1:
            raise ValueError("history_interval needs to be at least 1, default is 15 (in minutes)")
        return value

    def get_model_event(self) -> ModelEvent:
        return ModelEvent.POINT

    def get_model_event_type(self) -> EventType:
        return EventType.POINT_MODEL

    def update(self, **kwargs):
        super().update(**kwargs)

        point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(self.uuid)
        updated: bool = self.update_point_value(point_store, self.driver, 0)
        self.point_store = point_store

        if updated:
            self.publish_cov(self.point_store)

        return self

    def update_point_store(self, value: float, priority: int, value_raw: str, fault: bool, fault_message: str):
        self.update_priority_value(priority, value, value_raw)
        highest_priority_value = PriorityArrayModel.get_highest_priority_value(self.uuid)
        point_store = PointStoreModel(point_uuid=self.uuid,
                                      value_original=highest_priority_value,
                                      value_raw=value_raw if value_raw is not None else highest_priority_value,
                                      fault=fault,
                                      fault_message=fault_message)
        updated = self.update_point_value(point_store, self.driver)
        if updated:
            self.publish_cov(point_store)
        db.session.commit()

    def update_priority_value(self, priority, value, value_raw):
        if not priority:
            priority = 16
        if priority not in range(1, 17):
            raise ValueError('priority should be in range(1, 17)')
        if value_raw is not None and value is not None:
            raise ValueError('Invalid, cannot pass both value_raw and value')
        if priority:
            PriorityArrayModel.filter_by_point_uuid(self.uuid).update({f"_{priority}": value})
            db.session.commit()

    @classmethod
    def apply_offset(cls, original_value: float, value_offset: float, value_operation: MathOperation) -> float or None:
        """Do calculations on original value with the help of point details"""
        if original_value is None or value_operation is None:
            return original_value
        value = original_value
        if value_operation == MathOperation.ADD:
            value += value_offset
        elif value_operation == MathOperation.SUBTRACT:
            value -= value_offset
        elif value_operation == MathOperation.MULTIPLY:
            value *= value_offset
        elif value_operation == MathOperation.DIVIDE:
            value /= value_offset
        elif value_operation == MathOperation.BOOL_INVERT:
            value = not bool(value)
        return value

    @classmethod
    def apply_scale(cls, value: float, input_min: float, input_max: float, output_min: float, output_max: float) \
            -> float or None:
        if value is None or input_min is None or input_max is None or output_min is None or output_max is None:
            return value
        value = ((value - input_min) * (output_max - output_min)) / (input_max - input_min) + output_min
        return value

    @classmethod
    @abstractmethod
    def apply_point_type(cls, value: float) -> float:
        pass

    def publish_cov(self, point_store: PointStoreModel, device: DeviceModel = None, network: NetworkModel = None,
                    driver_name: str = None):
        if point_store is None:
            raise Exception('Point.publish_cov point_store cannot be None')
        if device is None:
            device = DeviceModel.find_by_uuid(self.device_uuid)
        if network is None:
            network = NetworkModel.find_by_uuid(device.network_uuid)
        if device is None or network is None:
            raise Exception(f'Cannot find network or device for point {self.uuid}')
        if driver_name is None:
            driver_name = network.driver.name

        if self.history_enable and self.history_type == HistoryType.COV and network.history_enable and \
                device.history_enable:
            PointStoreHistoryModel.create_history(point_store)

        from src.event_dispatcher import EventDispatcher
        EventDispatcher().dispatch_from_source(None, Event(EventType.POINT_COV, {
            'point': self,
            'point_store': point_store,
            'device': device,
            'network': network,
            'driver_name': driver_name
        }))
