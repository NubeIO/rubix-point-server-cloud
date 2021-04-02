from src import db
from src.drivers.enums.drivers import Drivers
from src.enums.model import ModelEvent
from src.enums.network_master_type import NetworkMasterType
from src.models.model_base import ModelBase
from src.services.event_service_base import EventType


class NetworkMasterModel(ModelBase):
    __tablename__ = 'networks_masters'

    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.Enum(NetworkMasterType), default=NetworkMasterType.INTEGRATION)
    networks = db.relationship('NetworkModel', cascade="all,delete", backref='network_master', lazy=True)

    # TODO: needs value for type CLOUD, to sync with EDGE (null for type EDGE, we don't have to sync)
    # site_uuid = db.Column(db.String, db.ForeignKey('site.uuid'), nullable=True)
    # device_uuid = db.Column(db.String, db.ForeignKey('device.uuid'), nullable=True)
    driver = db.Column(db.Enum(Drivers), default=Drivers.GENERIC)

    __mapper_args__ = {
        'polymorphic_identity': 'network_master',
        'polymorphic_on': driver
    }

    @classmethod
    def find_by_name(cls, network_master_name: str):
        results = cls.query.filter_by(name=network_master_name).first()
        return results

    def get_model_event(self) -> ModelEvent:
        return ModelEvent.NETWORK_MASTER

    def get_model_event_type(self) -> EventType:
        return EventType.NETWORK_MASTER_MODEL

    def set_fault(self, is_fault: bool):
        self.fault = is_fault
        db.session.commit()
