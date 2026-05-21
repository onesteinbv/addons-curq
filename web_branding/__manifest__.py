{
    "name": "CURQ Branding in backend",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Hidden",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "assets": {
        "web._assets_primary_variables": [
            (
                "before",
                "web/static/src/scss/primary_variables.scss",
                "web_branding/static/src/scss/primary.variables.scss",
            ),
            (
                "before",
                "web/static/src/webclient/navbar/navbar.variables.scss",
                "web_branding/static/src/scss/navbar.variables.scss",
            ),
        ],
        "web.assets_backend": [
            (
                "before",
                "web_responsive/static/src/components/apps_menu/apps_menu.scss",
                "web_branding/static/src/scss/appmenu.variables.scss",
            ),
            "web_branding/static/src/scss/appmenu.scss",
            "web_branding/static/src/scss/searchbar.scss",
        ],
    },
    "data": [
        "templates/layout.xml",
    ],
    "depends": [
        "web",
        "web_responsive",
    ],
}
