#!/bin/bash

BUILD_VERSION=`python get_version.py | sed 's/+/_/g'`
REGISTRY=$(( $1 -eq "TEAM" ? $NEXUS_DOCKER_REGISTRY : $NEXUS_DOCKER_STAGING ))

DOCKER_FILE=$(( $1 -eq "TEAM" ? Dockerfile : Dockerfile-CE ))

docker build --network=host -t "$REGISTRY/auth-proxy:$BUILD_VERSION" -f $DOCKER_FILE \
  && docker tag "$REGISTRY/auth-proxy:$BUILD_VERSION" "$REGISTRY/auth-proxy:latest" \
  && docker push "$REGISTRY/auth-proxy" \
  && echo "Successfully build and pushed auth-proxy to the $REGISTRY repository"
