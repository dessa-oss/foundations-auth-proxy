# foundations-auth-proxy

## Setup
By default the server runs on `http://0.0.0.0:5558`. This can be changed via the arguments.

**Arguments:**
 - '-H' or '--host': host to bind server (default: 0.0.0.0)
 - '-p' or '--port': port to bind server (default: 5000)
 - '-d' or '--debug': starts server in debug mode
 - '-n' or '--null': starts server as a null proxy - forwarding everything through without the need for authorization

You may also have to configure `proxy_config.yaml` with the proper `service_uri` information.

## Running Locally
Run `python -m auth_proxy` from the project root directory.

## Running in Docker
Build the image with `docker build -t us.gcr.io/foundations/authentication-proxy:X.X .`

To run the container without authorization (a null auth-proxy), run `docker run --network foundations-atlas -p 5558:5558 us.gcr.io/foundations/authentication-proxy:0.1 -n`.
To run with authorization enabled, run `docker run --network foundations-atlas -p 5558:5558 us.gcr.io/foundations/authentication-proxy:0.1`

## Configuration

There are two main files used to configure the proxy - proxy_config.yaml and route_mapping.yaml.

**proxy_config.yaml**

`service_uris` is a dictionary where the keys are the identifier for a service that the proxy can route to and the value is the service URI. The key _must_ be the same as the
corresponding key in route_mapping.yaml.

`supported_proxy_methods` is a list of the methods that the proxy route allows. _Flask requires specification of the methods a given route allows._

**route_mapping.yaml**

The keys of this file are the identifier for a services that will. The key _must_ be the same as the corresponding key under `service_uris` in proxy_config.yaml. The value
of each key is a list of excepted routes that the proxy can forward to.