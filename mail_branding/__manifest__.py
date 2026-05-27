{
    "name": "Mail Branding",
    "summary": "Mail Branding: Adapting to CURQ branding",
    "author": "Onestein",
    "website": "https://onestein.eu",
    "category": "Mail",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail",
    ],
    "data": ["data/company_colors.xml"],
    "installable": True,
    "post_init_hook": "update_curqbot_name_in_res_users",
    "uninstall_hook": "uninstall_hook",
    "auto_install": True,
}
