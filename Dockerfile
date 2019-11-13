#
# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Cole Clifford <c.clifford@dessa.com>, 11 2019
#

FROM python:3.7-alpine as base
LABEL maintainer="Cole Clifford"
LABEL version="0.1"

FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local

COPY . /app/auth-proxy/

WORKDIR /app/auth-proxy

EXPOSE 5558

ENTRYPOINT ["python", "-m", "auth_proxy", "-p 5558"]