#!/bin/bash

docker_registry=${DOCKER_REGISTRY:-foundations}


docker push \
  "${docker_registry}/auth-proxy" \
  && echo "Successfully pushed auth-proxy to the ${docker_registry} repository"
