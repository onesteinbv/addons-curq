# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account - Configuration",
    "version": "18.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "depends": [
        # BASE
        "account",
        # COMMUNITY
        # OCA currency
        "account_invoice_constraint_chronology",
        "currency_rate_update",
    ],
    "data": ["data/mail_template_data.xml"],
    "post_init_hook": "post_init_hook",
}
