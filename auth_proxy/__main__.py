"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Cole Clifford <c.clifford@dessa.com>, 11 2019
"""

from flask import Flask, request, Response
from flask_cors import CORS
from urllib.parse import urlparse
import requests


def get_args():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Starts a local docker scheduler')
    parser.add_argument('-H', '--host', type=str, default="0.0.0.0", help='host to bind server (default: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int, default=5558, help='port to bind server (default: 5558)')
    parser.add_argument('-d', '--debug', action='store_true', help='starts server in debug mode')
    parser.add_argument('-n', '--null', action='store_true', help='starts server as a null proxy - forwarding everything through without the need for authorization')

    return parser.parse_args(sys.argv[1:])


def _load_yaml(path):
    import yaml
    with open(path, 'r') as file:
        return yaml.load(file)


def _generate_route_mapping_rules(route_mapping):
    from werkzeug.routing import Map, Rule

    # Throwaway variable to take advantage of the routing library
    routing_map = Map()

    # Turn the route mapping into a mapping of Rules
    rules_map = {}
    for key in route_mapping:
        rules_map[key] = []
        for value in route_mapping[key]:
            rule = Rule(value)
            rule.bind(routing_map)
            rules_map[key].append(rule)
    return rules_map


def _is_path_in_rule_list(path, rule_list):
    for rule in rule_list:
        if rule.match(f"|/{path}") is not None:
            return True
    return False


def _get_proper_url(path):
    if _is_path_in_rule_list(path, rule_mapping["scheduler_rest_api"]):
        return proxy_config["service_uris"]["scheduler_rest_api"]
    elif _is_path_in_rule_list(path, rule_mapping["foundations_rest_api"]):
        return proxy_config["service_uris"]["foundations_rest_api"]
    else:
        return False


def _token_is_valid(headers):
    excluded_headers = ['content-length', 'content-type']
    headers = { key: value for key, value in headers.items() if key.lower() not in excluded_headers }
    response = requests.get(f"{proxy_config['service_uris']['foundations_rest_api']}/api/v2beta/auth/verify", headers=headers)
    try:
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


args = get_args()
app = Flask(__name__)
route_mapping = _load_yaml("route_mapping.yaml")
rule_mapping = _generate_route_mapping_rules(route_mapping)
proxy_config = _load_yaml("proxy_config.yaml")


@app.route("/")
def root():
    return "Welcome to the Foundations authentication proxy"


@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    return "Alive"


@app.route("/<path:path>", methods=proxy_config["supported_proxy_methods"])
def proxy(path=None):

    # Get the proper address based on the route mapping
    redirect_url = _get_proper_url(path)
    if not redirect_url:
        return Response("Cannot find that address in the proxies route mapping", status=500)
    full_redirect_url_with_path = f"{redirect_url}{urlparse(request.url).path}"

    # Resolve the token situation
    # For login and logout, token check should not be required
    if args.null or "login" in path or "logout" in path:
        token_is_valid = True
    else:
        token_is_valid = _token_is_valid(request.headers)

    # Check token from cookies
    if token_is_valid:

        # Forward on the response
        resp = requests.request(
            method=request.method,
            url=full_redirect_url_with_path,
            headers=request.headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        # Setup the response headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        # Create the response object
        response = Response(resp.content, resp.status_code, headers)
        return response
    else:
        return Response("Token is not valid", status=401)


if __name__ == "__main__":
    CORS(app)
    app.run(use_reloader=False, debug=args.debug, host=args.host, port=args.port, threaded=True)
