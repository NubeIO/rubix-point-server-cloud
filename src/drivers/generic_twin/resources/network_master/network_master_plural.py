from flask_restful.reqparse import request

from src.drivers.generic_twin.models.network_master import GenericTwinNetworkMasterModel
from src.drivers.generic_twin.resources.network_master.network_master_base import GenericTwinNetworkMasterBase, \
    generic_twin_network_master_marshaller


class GenericTwinNetworkMasterPlural(GenericTwinNetworkMasterBase):

    @classmethod
    def get(cls):
        return generic_twin_network_master_marshaller(GenericTwinNetworkMasterModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = GenericTwinNetworkMasterPlural.parser.parse_args()
        return generic_twin_network_master_marshaller(cls.add_network_master(data), request.args)
