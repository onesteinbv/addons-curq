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
            "web_branding/static/src/js/user_menu_items.esm.js",
            "web_branding/static/src/js/app_menu_preferences.esm.js",
            "web_branding/static/src/js/title_service.esm.js",
            "web_branding/static/src/xml/documentation_link.xml",
        ],
    },
    "data": [
        "templates/layout.xml",
    ],
    "depends": [
        "web",
        "web_responsive",
        "web_tour",
        "disable_odoo_online",  # Not a real dependency, but this module doesn't make sense without it.
    ],
}
