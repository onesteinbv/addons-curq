#!/bin/bash

# Update website_breadcrumb to remove breadcrumb_enabled
odoo -u website_breadcrumb --stop-after-init
# Uninstall website_share_filter_option_skype module
click-odoo-uninstall -c $ODOO_RC -d $DB_NAME -m website_share_filter_option_skype
