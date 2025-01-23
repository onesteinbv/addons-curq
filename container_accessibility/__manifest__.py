{
    "name": "Container Accessibility",
    "category": "Technical",
    "version": "16.0.1.0.0",
    "author": "Onestein BV",
    "website": "https://www.onestein.eu",
    "depends": [
        "privacy_lookup",
        "web_tour",
        "payment",
        "base_menu_visibility_restriction",
        "auth_oidc",
        "auditlog",
        "server_environment",
        "fs_storage",
        "fs_storage_backup",
        "fs_attachment",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir_rule.xml",
        "data/auditlog_rule_data.xml",
        "data/ir_cron_data.xml",
        "views/ir_module_module_view.xml",
        "menuitems.xml",
    ],
    "license": "AGPL-3",
}
