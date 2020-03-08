#!/bin/bash

docker_registry=${DOCKER_REGISTRY:-atlas}
BUILD_VERSION=`python get_version.py | sed 's/+/_/g'`
DOCKER_FILE="Dockerfile" && [[ $1 == "null" ]] && DOCKER_FILE="Dockerfile-null"

docker build \
  --network=host \
  -t "${docker_registry}/auth-proxy:$BUILD_VERSION" -f $DOCKER_FILE \
  . && \
  
docker tag \
  "${docker_registry}/auth-proxy:$BUILD_VERSION" \
  "${docker_registry}/auth-proxy:latest" && \

echo "Successfully built auth-proxy to the ${docker_registry} repository"
  
