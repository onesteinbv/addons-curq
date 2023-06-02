# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Services Based Organization - Install',
    'description': 'Services Based Organization - Install',
    'category': 'Technical Settings',
    'version': '16.0.1.0.0',
    'author': 'Onestein',
    'website': 'https://www.onestein.nl',
    'license': 'AGPL-3',
    'depends': [
        # Base
        'account',
        'account_edi',
        'account_edi_ubl_cii',
        'account_payment',
        'sale_timesheet',
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
        #loyalty',
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
        #payment_demo',
        'payment_custom',
        'phone_validation',
        'portal',
        'portal_rating',
        'product',
        'product_margin',
        'project',
        'project_timesheet_holidays',
        'project_hr_expense',
        'project_purchase',
        'purchase',
        'purchase_stock',
        'rating',
        'report_xlsx',
        'resource',
        'sale',
        'sale_loyalty',
        'sale_crm',
        'sale_expense',
        'sale_management',
        'sale_project',
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
        'website_sale_loyalty',
        'website_sale_stock',
        'website_sms',

        # Community
        'account_credit_control',
        "account_invoice_overdue_reminder",
        'account_reconcile_oca',
        'account_usability',
        'account_financial_report',
        'account_asset_management',
        'account_banking_sepa_credit_transfer',
        'account_banking_sepa_direct_debit',
        'account_fiscal_position_vat_check',
        'account_fiscal_year',
        'account_invoice_constraint_chronology',
        'account_journal_lock_date',
        'account_lock_date_update',
        'account_move_line_purchase_info',
        'account_move_line_sale_info',
        'account_move_line_tax_editable',
        'account_move_name_sequence',
        'account_move_print',
        'account_usability',
        'base_vat_optional_vies',
        'product_category_tax',
        'account_move_tier_validation',
        'account_reconcile_oca',
        'account_statement_import_online_paypal',
        #'website_matomo_tag_manager',
        'account_statement_import_file_reconcile_oca',
        'account_statement_import_camt',
        'account_statement_import_online',
        'account_statement_import_online_ponto',
        'auditlog',
        'base_fontawesome',
        'base_user_role',
        'currency_rate_update',
        'date_range',
        'disable_odoo_online',
        'hr_timesheet_sheet',
        'l10n_nl_bank',
        'l10n_nl_bsn',
        'l10n_nl_postcode',
        'l10n_nl_tax_statement',
        'mail_tracking',
        'mass_mailing_partner',
        'partner_external_map',
        'project_timeline',
        #project_role',
        'report_qr',
        'report_qweb_parameter',
        'report_wkhtmltopdf_param',
        'report_xlsx',
        'report_xlsx_helper',
        'remove_odoo_enterprise',
        #'web_widget_dropdown_dynamic',
        'web_responsive',
        'web_no_bubble',
        'web_search_with_and',
        'web_widget_x2many_2d_matrix',
        'web_timeline',
        'website_odoo_debranding',

        # Onestein
        #base_municipality'
        #mass_mailing_membership_committee',
        #mass_mailing_membership_section',
        #'payment_mollie_fix',
        #'mass_mailing_help',
        #membership_committee',
        #membership_hr',
        #membership_hr_recruitment',
        #membership_section',
        #project_role_members',
        'nextcloud_odoo_sync',
        'web_editor_fontawesome',
        #website_event_external_map',
        #website_event_share_filter_option',
        #website_hide_navbar_technical',
        #website_mass_mailing_membership_section',
        #website_membership_registration',
        #website_membership_section',
        #website_project',
        #website_project_role_members',
        #website_sale_share_filter_option',
        #website_share_blogger',
        #website_share_diaspora',
        #website_share_filter_option_blogger',
        #website_share_filter_option_diaspora',
        #website_share_filter_option_friendica',
        #website_share_filter_option_mastodon',
        #website_share_filter_option_pleroma',
        #website_share_filter_option_reddit',
        #website_share_filter_option_skype',
        #website_share_filter_option_snapchat',
        #website_share_filter_option_technical',
        #website_share_filter_option_telegram',
        #website_share_filter_option_tumblr',
        #website_share_filter_option_wordpress',
        #website_share_friendica',
        #website_share_mastodon',
        #website_share_pleroma',
        #website_share_reddit',
        #website_share_skype',
        #website_share_snapchat',
        #website_share_telegram',
        #website_share_tumblr',
        #website_share_wordpress',
        #website_snippet_dynamic_link',
        #website_snippet_openstreetmap',
        #website_two_steps_share_technical',

        # 3rd-Party
        'mollie_account_sync',
        #'mollie_subscription_ept',
        'payment_mollie_official',
        'l10n_nl_rgs',

    ],
    'data': [],
}
