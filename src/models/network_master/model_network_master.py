from src import db
from src.drivers.enums.drivers import Drivers
from src.enums.model import ModelEvent
from src.enums.network_master_type import NetworkMasterType
from src.models.model_base import ModelBase
from src.services.event_service_base import EventType


class NetworkMasterModel(ModelBase):
    __tablename__ = 'networks_masters'
    global_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    client_id = db.Column(db.String(80), nullable=True)
    client_name = db.Column(db.String(80), nullable=False)
    site_id = db.Column(db.String(80), nullable=False)
    site_name = db.Column(db.String(80), nullable=False)
    device_id = db.Column(db.String(80), nullable=False)
    device_name = db.Column(db.String(80), nullable=False)
    site_address = db.Column(db.String(80), nullable=False)
    site_city = db.Column(db.String(80), nullable=False)
    site_state = db.Column(db.String(80), nullable=False)
    site_zip = db.Column(db.String(80), nullable=False)
    site_country = db.Column(db.String(80), nullable=False)
    site_lat = db.Column(db.String(80), nullable=False)
    site_lon = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(NetworkMasterType), default=NetworkMasterType.INTEGRATION)
    networks = db.relationship('NetworkModel', cascade="all,delete", backref='network_master', lazy=True)
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
