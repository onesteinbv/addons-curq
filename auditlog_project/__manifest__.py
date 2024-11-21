# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Audit Log Project",
    "summary": "Adds audit log rules for recording deletions for projects and tasks",
    "version": "16.0.1.0.0",
    "author": "Onestein",
    "license": "AGPL-3",
    "category": "Tools",
    "depends": ["auditlog", "project"],
    "data": [],
    "application": True,
    "installable": True,
    "auto_install": True,
    "post_init_hook": "post_init_hook",
}
