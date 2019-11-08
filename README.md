# foundations-auth-proxy

### Setup
By default the server runs on `http://0.0.0.0:5558`. This can be changed via the arguments.

**Arguments:**
 - '-H' or '--host': host to bind server (default: 0.0.0.0)
 - '-p' or '--port': port to bind server (default: 5000)
 - '-d' or '--debug': starts server in debug mode
 - '-n' or '--null': starts server as a null proxy - forwarding everything through without the need for authorization

You may also have to configure `proxy_config.yaml` with the proper `service_uri` information.

### Running locally
Run `python -m auth_proxy` from the project root directory.

### Running in Docker
Build the image with `docker build -t us.gcr.io/foundations/authentication-proxy:X.X .`

To run the container without authorization (a null auth-proxy), run `docker run --network foundations-atlas -p 5558:5558 us.gcr.io/foundations/authentication-proxy:0.1 -n`.
To run with authorization enabled, run `docker run --network foundations-atlas -p 5558:5558 us.gcr.io/foundations/authentication-proxy:0.1`