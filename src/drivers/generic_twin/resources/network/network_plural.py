from flask_restful.reqparse import request

from src.drivers.generic_twin.models.network import GenericTwinNetworkModel
from src.drivers.generic_twin.resources.network.network_base import generic_twin_network_marshaller, \
    GenericTwinNetworkBase


class GenericTwinNetworkPlural(GenericTwinNetworkBase):

    @classmethod
    def get(cls):
        return generic_twin_network_marshaller(GenericTwinNetworkModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = GenericTwinNetworkPlural.parser.parse_args()
        return generic_twin_network_marshaller(cls.add_network(data), request.args)
