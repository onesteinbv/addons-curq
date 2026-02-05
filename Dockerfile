# syntax=docker/dockerfile:1-labs
FROM python:3.11-bookworm AS pack

COPY repos.yaml repos.yaml
COPY package.txt package.txt
COPY scripts/pack.py pack.py

COPY --parents \
	account_configuration \
	account_install \
	account_statement_import_online_ponto_log \
	account_statement_import_online_ponto_statement_creation_mode \
	account_statement_import_sheet_file_sheet_mappings \
	base_customer_company \
	base_customer_user \
	base_module_bundle \
	base_onboarding \
	container_accessibility \
	container_install \
	container_s3 \
	crm_install \
	crypto_currency_install \
	digest_configuration \
	digest_disable \
	event_install \
	helpdesk_install \
	helpdesk_project_install \
	hr_accessibility \
	hr_install \
	l10n_de_install \
	l10n_nl_hr_expense \
	l10n_nl_hr_install \
	l10n_nl_hr_recruitment \
	l10n_nl_install \
	l10n_nl_rgs_usability \
	mass_mailing_force_dedicated_server \
	mass_mailing_install \
	mass_mailing_website_install \
	membership_development_install \
	membership_install \
	project_install \
	sale_install \
	stock_install \
	subscription_install \
	survey_install \
	website_event_install \
	website_install \
	website_membership_install \
	website_onboarding \
	website_sale_install \
	stock_account_install \
	sale_stock_install \
	sales_team_update \
	resource_booking_install \
    spreadsheet_oca_ux \
	./

RUN apt-get install git -y
RUN pip install --no-cache-dir git-aggregator==4.0.2 click==8.1.8
# Configure dummy git user to avoid errors
RUN git config --global user.name "bot" && \
    git config --global user.email "bot@onestein.nl" && \
    gitaggregate -c repos.yaml
RUN python3 pack.py --location . --package-file "package.txt" --destination "package"

FROM ubuntu:22.04 AS wheels
COPY --from=pack ./odoo/requirements.txt /requirements.txt
COPY requirements.txt /curq-requirements.txt
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y python3.12 cython3 libldap2-dev libpq-dev libsasl2-dev gcc python3.12-dev python3.12-venv libcairo2-dev libjpeg-dev libgif-dev \
    && python3.12 -m ensurepip --upgrade \
    && pip3.12 install -U wheel setuptools \
    && sed -i -E "s/(gevent==)21\.8\.0( ; sys_platform != 'win32' and python_version == '3.10')/\122.10.2\2/;s/(greenlet==)1.1.2( ; sys_platform != 'win32' and python_version == '3.10')/\12.0.2\2/" /requirements.txt \
    && pip3.12 wheel -r /requirements.txt -r /curq-requirements.txt --wheel-dir=/wheels

FROM ghcr.io/onesteinbv/odoo-docker:18.0-1b836859b226c078e6331b066f18af147f8e7830 AS base
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
COPY test-requirements.txt /test-requirements.txt
RUN pip install --no-cache-dir -r /test-requirements.txt
RUN apt-get update && apt-get install expect -y
ENTRYPOINT [ "/bin/bash" ]
