#!/bin/bash

BUILD_VERSION=`python get_version.py | sed 's/+/_/g'`
echo $1
DOCKER_FILE="Dockerfile" && [[ $1 -eq "null" ]] && DOCKER_FILE="Dockerfile-null"

docker build --network=host -t "$NEXUS_DOCKER_REGISTRY/auth-proxy:$BUILD_VERSION" -f $DOCKER_FILE . \
  && docker tag "$NEXUS_DOCKER_REGISTRY/auth-proxy:$BUILD_VERSION" "$NEXUS_DOCKER_REGISTRY/auth-proxy:latest" \
  && docker push "$NEXUS_DOCKER_REGISTRY/auth-proxy" \
  && echo "Successfully build and pushed auth-proxy to the $NEXUS_DOCKER_REGISTRY repository"
