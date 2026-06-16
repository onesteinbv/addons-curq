{
    "name": "Sale Branding",
    "summary": "Remove Odoo sample quotation button/branding from quotation views.",
    "description": """
        This module removes the 'Check a sample. It's clean!' button and the
        onboarding video helper from the empty-state quotation views in Odoo Sales.
    """,
    "category": "Sales",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Onestein",
    "website": "https://onestein.eu",
    "depends": [
        "sale",
    ],
    "data": [
        "views/sale_branding_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sale_branding/static/src/xml/sale_action_helper.xml",
        ],
    },
    "auto_install": True,
}
