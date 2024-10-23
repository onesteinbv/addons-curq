# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Onboarding",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Extra Tools",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["multi_step_wizard", "web", "mail"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "wizards/onboarding_wizard_view.xml",
        "views/base_document_layout_view.xml",
    ],
    "demo": ["demo/res_groups_demo.xml"],
    "assets": {
        "web.assets_backend": [
            "base_onboarding/static/src/js/backend.esm.js",
        ],
    },
}
