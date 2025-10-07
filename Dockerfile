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
	base_mail_security \
	base_module_bundle \
	base_onboarding \
	container_accessibility \
	container_install \
	container_s3 \
	crm_install \
	digest_configuration \
	digest_disable \
	event_install \
	helpdesk_install \
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
	survey_install \
	website_event_install \
	website_install \
	website_membership_install \
	website_onboarding \
	website_sale_install \
	stock_account_install \
	sale_stock_install \
	resource_booking_install \
	./

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

FROM ghcr.io/onesteinbv/odoo-docker:18.0-42d259caebe7479cc9b36e6b86d191e2c97b6f05 AS base
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
