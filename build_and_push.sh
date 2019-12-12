#!/bin/bash

export build_version=`python get_version.py | sed 's/+/_/g'`
registry=${NEXUS_DOCKER_REGISTRY:-docker.shehanigans.net}


docker build --network=host -t "$registry/auth-proxy:$build_version" . \
  && docker tag "$registry/auth-proxy:$build_version" "$registry/auth-proxy:latest" \
  && docker push "$registry/auth-proxy" \
  && echo "Successfully build and pushed auth-proxy to the $registry repository"