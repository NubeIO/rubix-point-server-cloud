from flask import request, Blueprint
from flask_restful import abort
from rubix_http.method import HttpMethod
from rubix_http.request import gw_mqtt_slave_request

from src.discover.remote_device_registry import RemoteDeviceRegistry

bp_slave_proxy = Blueprint("slave_proxy", __name__, url_prefix='/slave')
methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']


@bp_slave_proxy.route("/<path:_>", methods=methods)
def slave_proxy_handler(_):
    url_parts = request.full_path.split("/")
    requested_url_prefix = "{}".format(url_parts[1])
    if requested_url_prefix != "slave" or len(url_parts) <= 3:
        abort(404)
    del url_parts[0]
    del url_parts[0]
    slave_global_uuid: str = url_parts[0]
    del url_parts[0]
    url = "/".join(url_parts)
    if slave_global_uuid in RemoteDeviceRegistry().registered_available_devices_global_uuids:
        return gw_mqtt_slave_request(
            slave_global_uuid=slave_global_uuid,
            api=url,
            body=request.get_json(),
            http_method=HttpMethod[request.method.upper()])
    return {"message": f"Slave with global_uuid {slave_global_uuid} is not active!"}, 404
