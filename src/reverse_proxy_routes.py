from flask import request, Blueprint
from flask_restful import abort
from rubix_http.method import HttpMethod
from rubix_http.request import gw_mqtt_slaves_request

bp_slaves_request = Blueprint("slaves_request", __name__, url_prefix='/slaves')
methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']


@bp_slaves_request.route("/<path:_>", methods=methods)
def slaves_request_handler(_):
    url_parts = request.full_path.split("/")
    requested_url_prefix = "{}".format(url_parts[1])
    if requested_url_prefix != "slaves":
        abort(404)
    del url_parts[0]
    del url_parts[0]
    url = "/".join(url_parts)
    return gw_mqtt_slaves_request(api=url, body=request.get_json(), http_method=HttpMethod[request.method.upper()])
