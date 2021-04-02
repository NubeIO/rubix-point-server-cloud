from src.drivers.enums.drivers import Drivers
from src.models.network_master.model_network_master_mixin import NetworkMasterMixinModel


class GenericTwinNetworkMasterModel(NetworkMasterMixinModel):
    __tablename__ = 'generic_twin_networks_masters'

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC_TWIN
