# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Services Based Organization - Install',
    'description': 'Services Based Organization - Install',
    'category': 'Technical Settings',
    'version': '15.0.1.0.0',
    'author': 'Onestein',
    'website': 'https://www.onestein.nl',
    'license': 'AGPL-3',
    'depends': [
        # Base
        'account',
        'account_edi',
        'account_edi_facturx',
        'account_edi_ubl_cii',
        'account_payment',
        'account_sale_timesheet',
        'account_qr_code_sepa',
        'analytic',
        #association',
        'attachment_indexation',
        'auth_signup',
        'auth_totp',
        'auth_totp_mail',
        'auth_totp_portal',
        'barcodes',
        'base_address_extended',
        'base_automation',
        'base_geolocalize',
        'base_iban',
        'base_import',
        'base_setup',
        'base_vat',
        'board',
        'calendar',
        'calendar_sms',
        'contacts',
        'contract',
        'contract_payment_mode',
        #coupon',
        'crm',
        'crm_iap_enrich',
        'crm_iap_mine',
        'crm_sms',
        'digest',
        #event',
        #event_crm',
        #event_crm_sale',
        #event_sale',
        #event_sms',
        'fetchmail',
        'google_recaptcha',
        'helpdesk_mgmt',
        'helpdesk_mgmt_project',
        'hr',
        'hr_contract',
        'hr_expense',
        'hr_holidays',
        'hr_org_chart',
        #hr_recruitment',
        'hr_timesheet',
        'http_routing',
        'iap',
        'iap_crm',
        'iap_mail',
        'l10n_multilang',
        'l10n_nl',
        'link_tracker',
        'mail',
        'mail_bot',
        'mail_bot_hr',
        'mass_mailing',
        'mass_mailing_crm',
        #mass_mailing_event',
        'mass_mailing_sale',
        #membership',
        'mis_builder',
        'mis_builder_budget',
        'partner_autocomplete',
        'payment',
        #payment_test',
        'payment_transfer',
        'phone_validation',
        'portal',
        'portal_rating',
        'product',
        'product_margin',
        'project',
        'project_account',
        'project_timesheet_holidays',
        'project_hr_expense',
        'project_purchase',
        'purchase',
        'purchase_stock',
        'rating',
        'report_xlsx',
        'resource',
        'sale',
        'sale_coupon',
        'sale_crm',
        'sale_expense',
        'sale_management',
        'sale_project',
        'sale_project_account',
        'sale_purchase',
        'sale_purchase_stock',
        'sale_sms',
        'sale_stock',
        'sales_team',
        'sale_timesheet',
        'sms',
        'snailmail',
        'snailmail_account',
        'social_media',
        'stock',
        'stock_account',
        'stock_sms',
        'uom',
        'utm',
        'web_editor',
        'web_kanban_gauge',
        'web_tour',
        'web_unsplash',
        'website',
        'website_blog',
        'website_crm',
        'website_crm_partner_assign',
        'website_crm_sms',
        'website_customer',
        #website_event',
        #website_event_crm',
        #website_event_sale',
        #website_event_track',
        #website_form_project',
        'website_google_map',
        #website_hr_recruitment',
        #website_links',
        'website_mail',
        'website_mass_mailing',
        #website_membership',
        'website_partner',
        'website_payment',
        'website_sale',
        'website_sale_coupon',
        'website_sale_stock',
        'website_sms',

        # Community
        'account_credit_control',
        "account_invoice_overdue_reminder",
        'account_reconciliation_widget',
        'account_usability',
        'account_financial_report',
        'account_asset_management',
        'account_asset_management_menu',
        'account_balance_line',
        'account_banking_sepa_credit_transfer',
        'account_banking_sepa_direct_debit',
        'account_fiscal_position_vat_check',
        'account_fiscal_year',
        'account_invoice_constraint_chronology',
        'account_journal_lock_date',
        'account_lock_date_update',
        'account_move_force_removal',
        'account_move_line_menu',
        'account_move_line_purchase_info',
        'account_move_line_sale_info',
        'account_move_line_tax_editable',
        'account_move_name_sequence',
        'account_move_print',
        'account_usability',
        'base_vat_optional_vies',
        'product_category_tax',
        'account_move_tier_validation',
        'account_move_tier_validation_forward',
        'account_reconciliation_widget',
        'account_statement_import_online_paypal',
        'website_analytics_matomo',
        'account_statement_import',
        'account_statement_import_camt',
        'account_statement_import_online',
        'account_statement_import_online_ponto',
        'auditlog',
        'base_fontawesome',
        'currency_rate_update',
        'date_range',
        'disable_odoo_online',
        'hr_timesheet_sheet',
        'l10n_nl_bank',
        'l10n_nl_bsn',
        'l10n_nl_postcode',
        'l10n_nl_tax_statement',
        'l10n_nl_xaf_auditfile_export',
        'mail_tracking',
        'mass_mailing_partner',
        'partner_external_map',
        'project_timeline',
        'report_qr',
        'report_qweb_parameter',
        'report_wkhtmltopdf_param',
        'report_xlsx',
        'report_xlsx_helper',
        'remove_odoo_enterprise',
        'web_widget_dropdown_dynamic',
        'web_responsive',
        'web_no_bubble',
        'web_search_with_and',
        'web_widget_x2many_2d_matrix',
        'web_timeline',
        'website_odoo_debranding',
        'website_local_fonts',

        # Onestein
        'mass_mailing_help',
        'nextcloud_odoo_sync',
        'web_editor_fontawesome',

        # 3rd-Party
        'mollie_account_sync',
        'mollie_subscription_ept',
        'payment_mollie_official',
        'l10n_nl_rgs',
        'l10n_nl_rgs_asset',

    ],
    'data': [],
}
