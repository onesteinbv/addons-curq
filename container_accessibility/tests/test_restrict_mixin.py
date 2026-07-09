from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestRestrictMixin(TransactionCase):
    def test_restrict_mixin_without_domain(self):
        restricted_user = self.env["res.users"].create(
            {
                "name": "Restricted User",
                "login": "restricted_user",
                "role_id": self.ref("container_accessibility.role_administrator"),
            }
        )

        current_count = self.env["ir.ui.menu"].search_count([])
        with self.assertRaises(AccessError):
            self.env["ir.ui.menu"].with_user(restricted_user).create(
                {
                    "name": "New menu",
                }
            )
        new_count = self.env["ir.ui.menu"].search_count([])
        self.assertEqual(
            new_count, current_count, "Should not have been able to create a menu"
        )

        some_menu = self.env.ref("base.next_id_2")
        current_name = some_menu.name
        with self.assertRaises(AccessError):
            some_menu.with_user(restricted_user).write({"name": "Doesn't change"})
        self.assertEqual(
            some_menu.name, current_name, "Should not have been able to update the menu"
        )

        with self.assertRaises(AccessError):
            some_menu.with_user(restricted_user).unlink()

    def test_restrict_mixin_with_domain(self):
        restricted_user = self.env["res.users"].create(
            {
                "name": "Restricted User",
                "login": "restricted_user",
                "role_id": self.ref("container_accessibility.role_administrator"),
            }
        )
        real_admin = self.env.ref("base.user_admin")

        # Should be able to create a record with private=False since _get_restrict_domain returns a domain that allows it
        current_count = self.env["auth.oauth.provider"].search_count([])
        oauth_provider = (
            self.env["auth.oauth.provider"]
            .with_user(restricted_user)
            .create(
                {
                    "private": False,
                    "name": "Support oauth",
                    "auth_endpoint": "http://none",
                    "body": "Support Login",
                    "role_id": self.ref("container_accessibility.role_administrator"),
                }
            )
        )
        new_count = self.env["auth.oauth.provider"].search_count([])
        self.assertEqual(new_count, current_count + 1)
        current_count = new_count
        with self.assertRaises(AccessError):
            self.env["auth.oauth.provider"].with_user(restricted_user).create(
                {
                    "private": True,
                    "name": "Support oauth",
                    "auth_endpoint": "http://none",
                    "body": "Support Login",
                    "role_id": self.ref("container_accessibility.role_administrator"),
                }
            )
        new_count = self.env["auth.oauth.provider"].search_count([])
        self.assertEqual(
            new_count,
            current_count,
            "Should not have been able to create a record with private=True",
        )

        with self.assertRaises(AccessError):
            oauth_provider.write({"private": True})

        oauth_provider.with_user(real_admin).write({"private": True})
        with self.assertRaises(AccessError):
            oauth_provider.unlink()

        oauth_provider.with_user(real_admin).write({"private": False})
        oauth_provider.write(
            {
                "name": "Support oauth updated",
            }
        )
        self.assertEqual(
            oauth_provider.name,
            "Support oauth updated",
            "Should have been able to update the record with private=False",
        )
        oauth_provider.with_user(restricted_user).unlink()
        self.assertFalse(
            oauth_provider.exists(),
            "Should have been able to delete the record with private=False",
        )
