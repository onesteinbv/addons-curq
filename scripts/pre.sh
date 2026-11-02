#!/bin/bash

# Update website_breadcrumb to remove breadcrumb_enabled, helpdesk_mgmt to resolve issue with field helpdesk_mgmt_portal_select_category not found
odoo -u website_breadcrumb,helpdesk_mgmt --stop-after-init
