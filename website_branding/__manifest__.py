{
    "name": "CURQ Branding in frontend",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Website",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "website",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "website_branding/static/src/scss/primary_variables.scss"
        ],
        "website.assets_editor": [
            (
                "after",
                "website/static/src/client_actions/*/*.xml",
                "website_branding/static/src/scss/configurator.scss",
            ),
            (
                "after",
                "website/static/src/systray_items/*",
                "website_branding/static/src/scss/systray.scss",
            ),
        ],
    },
    "data": [
        "data/website_data.xml",
    ],
    "auto_install": True,
}
