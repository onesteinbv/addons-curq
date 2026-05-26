{
    "name": "Release Notes",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Extra Tools",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web", "base_setup"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/release_note_wizard_view.xml",
        "views/res_config_settings_view.xml",
        "templates/release_note.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "release_note/static/src/js/backend.esm.js",
            "release_note/static/src/scss/backend.scss",
        ],
    },
    "external_dependencies": {
        "python": [
            "markdown",
        ],
    },
}
