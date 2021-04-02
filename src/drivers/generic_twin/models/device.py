from src.drivers.enums.drivers import Drivers

from src.models.device.model_device_mixin import DeviceMixinModel


class GenericTwinDeviceModel(DeviceMixinModel):
    __tablename__ = 'generic_twin_devices'

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC_TWIN
