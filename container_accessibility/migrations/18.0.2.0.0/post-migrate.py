from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    group_restricted = env.ref("container_accessibility.group_restricted")
    role_manager = env.ref("container_accessibility.role_manager")
    role_administrator = env.ref("container_accessibility.role_administrator")
    role_guest = env.ref("container_accessibility.role_guest")

    # Assign guest role to portal users
    portal_users = env["res.users"].search([("share", "=", True)])
    portal_users.write({"role_id": role_guest.id})

    # Assign restricted users without private oauth to the manager role
    normal_users = env["res.users"].search(
        [
            ("share", "=", False),
            ("oauth_provider_id", "=", False),
            ("groups_id", "in", group_restricted.ids),
        ]
    )
    normal_users.write({"role_id": role_manager.id})

    # Assign restricted users with private oauth to the administrator role
    admin_users = env["res.users"].search(
        [
            ("share", "=", False),
            ("oauth_provider_id", "!=", False),
            ("oauth_provider_id.private", "=", True),
            ("groups_id", "in", group_restricted.ids),
        ]
    )
    admin_users.write({"role_id": role_administrator.id})
