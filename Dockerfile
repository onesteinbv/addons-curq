# syntax=docker/dockerfile:1-labs
FROM python:3.11-bookworm AS pack

COPY repos.yaml repos.yaml
COPY package.txt package.txt
COPY scripts/pack.py pack.py

# TODO: Should we move modules in repostory to a singular directory to make this easier?
COPY --parents \
	account_configuration \
	account_financial_consolidation_report \
	account_install \
	account_statement_import_online_ponto_log \
	account_statement_import_online_ponto_statement_creation_mode \
	account_statement_import_sheet_file_sheet_mappings \
	base_customer_company \
	base_customer_user \
	base_mail_security \
	base_module_bundle \
	base_onboarding \
	base_partner_security \
	base_user_limit \
	consolidation_account \
	container_accessibility \
	container_hr_recruitment \
	container_install \
	container_install_basis \
	container_s3 \
	crm_install \
	digest_configuration \
	digest_disable \
	event_install \
	helpdesk_install \
	hr_accessibility \
	hr_install \
	l10n_nl_hr_expense \
	l10n_nl_hr_recruitment \
	l10n_nl_rgs_usability \
	mass_mailing_force_dedicated_server \
	mass_mailing_install \
	membership_accessibility \
	membership_accessibility_mass_mailing_membership_group \
	membership_accessibility_website_project_role_members \
	membership_development_install \
	membership_install \
	multi_company_disable \
	project_install \
	sale_install \
	spreadsheet_oca_ux \
	stock_install \
	survey_install \
	website_event_install \
	website_install \
	website_membership_install \
	website_onboarding \
	website_sale_install \
	stock_account_install \
	./

RUN apt-get install git -y
RUN pip install --no-cache-dir git-aggregator==4.0.2 click==8.1.8
RUN gitaggregate -c repos.yaml
RUN python3 pack.py --location . --package-file "package.txt" --destination "package"

FROM ghcr.io/onesteinbv/odoo-docker:latest
COPY --from=pack ./odoo /odoo/src/odoo
COPY --from=pack ./package /odoo/custom
COPY ./scripts /odoo/scripts
COPY requirements.txt /odoo/custom/requirements.txt
RUN pip install --no-cache-dir -r /odoo/src/odoo/requirements.txt -f https://wheelhouse.acsone.eu/manylinux2014
# TODO: Fix dependency conflict with /odoo/src/odoo/requirements.txt and /odoo/custom/requirements.txt
RUN pip install --no-cache-dir -r /odoo/custom/requirements.txt
RUN pip install -e /odoo/src/odoo
