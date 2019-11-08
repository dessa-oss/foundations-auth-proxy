#
# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Cole Clifford <c.clifford@dessa.com>, 11 2019
#

FROM python:3.6-alpine

MAINTAINER Cole Clifford version: 0.1

COPY ./requirements.txt /app/requirements.txt

RUN pip install --requirement /app/requirements.txt

COPY . /app/auth-proxy/

WORKDIR /app/auth-proxy

EXPOSE 5558

ENTRYPOINT ["python", "-m", "auth_proxy", "-p 5558"]