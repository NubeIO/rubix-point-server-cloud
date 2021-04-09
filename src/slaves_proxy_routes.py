from typing import List

from flask import request, Blueprint
from flask_restful import abort
from rubix_http.method import HttpMethod
from rubix_http.request import gw_mqtt_slaves_multicast_request

from src.discover.remote_device_registry import RemoteDeviceRegistry

bp_slaves_proxy = Blueprint("slaves_proxy", __name__, url_prefix='/slaves')
methods = ['GET']


@bp_slaves_proxy.route("/<path:_>", methods=methods)
def slaves_proxy_handler(_):
    url_parts = request.full_path.split("/")
    requested_url_prefix = "{}".format(url_parts[1])
    if requested_url_prefix != "slaves":
        abort(404)
    del url_parts[0]
    del url_parts[0]
    url = "/".join(url_parts)
    registered_available_devices_global_uuids: List[
        str] = RemoteDeviceRegistry().registered_available_devices_global_uuids
    if registered_available_devices_global_uuids:
        return gw_mqtt_slaves_multicast_request(
            slaves_global_uuids=registered_available_devices_global_uuids,
            api=url,
            body=request.get_json(),
            http_method=HttpMethod[request.method.upper()])
    return {"message": "Registered devices are not available or haven't registered yet!"}, 404
