{
    "name": "Membership Branding",
    "summary": "Remove Odoo Branding from membership views.",
    "description": """
        This module removes the 'Odoo' branding from membership views.
    """,
    "category": "Memberships",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://onestein.eu",
    "author": "Onestein",
    "depends": [
        "membership",
    ],
    "data": [
        "views/membership_branding_views.xml",
    ],
    "installable": True,
    "application": False,
}
