from src.drivers.enums.drivers import Drivers

from src.models.network.model_network_mixin import NetworkMixinModel


class GenericTwinNetworkModel(NetworkMixinModel):
    __tablename__ = 'generic_twin_networks'

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC_TWIN
