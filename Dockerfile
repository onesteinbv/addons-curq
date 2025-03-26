# syntax=docker/dockerfile:1-labs
FROM python:3.11-bookworm AS pack

COPY repos.yaml repos.yaml
COPY package.txt package.txt
COPY scripts/pack.py pack.py

RUN apt-get install git -y
RUN pip install --no-cache-dir git-aggregator==4.0.2 click==8.1.8
RUN gitaggregate -c repos.yaml
RUN python3 pack.py --location . --package-file "package.txt" --destination "package"

FROM ubuntu:22.04 AS wheels
COPY --from=pack ./odoo/requirements.txt /requirements.txt
COPY requirements.txt /curq-requirements.txt
RUN apt-get update \
    && apt-get install -y python3-pip cython3 python3 libldap2-dev libpq-dev libsasl2-dev python3-requests gcc python3-dev \
    && pip install -U pip wheel setuptools \
    && sed -i -E "s/(gevent==)21\.8\.0( ; sys_platform != 'win32' and python_version == '3.10')/\122.10.2\2/;s/(greenlet==)1.1.2( ; sys_platform != 'win32' and python_version == '3.10')/\12.0.2\2/" /requirements.txt \
    && pip wheel -r /requirements.txt -r /curq-requirements.txt --wheel-dir=/wheels

FROM ghcr.io/onesteinbv/odoo-docker:18.0-f26b413b06aab4f57720351348b7bcf5a4385b2d AS base
COPY --from=pack ./odoo /odoo/src/odoo
COPY --from=pack ./package /odoo/custom
COPY --from=wheels ./wheels /odoo/wheels
COPY --from=wheels /curq-requirements.txt /odoo/custom/requirements.txt
COPY --from=wheels /requirements.txt /odoo/src/odoo/requirements.txt
COPY ./scripts /odoo/scripts
RUN pip install --no-cache-dir -r /odoo/src/odoo/requirements.txt -r /odoo/custom/requirements.txt --find-links /odoo/wheels
RUN pip install -e /odoo/src/odoo
RUN rm -rf /odoo/wheels

FROM base AS ci
RUN pip install --no-cache-dir manifestoo checklog-odoo odoo-test-helper
RUN apt-get update && apt-get install expect -y
ENTRYPOINT [ "/bin/bash" ]
