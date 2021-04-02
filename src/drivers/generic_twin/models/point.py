from src import db
from src.drivers.enums.drivers import Drivers
from src.drivers.generic_twin.enums.point.points import GenericPointType
from src.models.point.model_point_mixin import PointMixinModel


class GenericTwinPointModel(PointMixinModel):
    __tablename__ = 'generic_twin_points'

    type = db.Column(db.Enum(GenericPointType), nullable=False, default=GenericPointType.FLOAT)
    unit = db.Column(db.String, nullable=True)

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC_TWIN

    @classmethod
    def apply_point_type(cls, value: float):
        point = GenericTwinPointModel.find_by_uuid(cls.uuid)
        if point is not None and value is not None:
            if point.type == GenericPointType.STRING:
                value = None
            elif point.type == GenericPointType.INT:
                value = round(value, 0)
            elif point.type == GenericPointType.BOOL:
                value = float(bool(value))
        return value
