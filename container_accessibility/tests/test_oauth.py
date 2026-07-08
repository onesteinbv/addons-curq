from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestOauth(TransactionCase):
    def test_new_user_with_private_provider(self):
        private_provider = self.env["auth.oauth.provider"].create(
            {
                "private": True,
                "name": "Support oauth",
                "role_id": self.ref("container_accessibility.role_administrator"),
                "auth_endpoint": "http://none",
                "body": "Support Login",
            }
        )
        new_user = self.env["res.users"]._create_user_from_template(
            {
                "login": "support1",
                "name": "Support 1",
                "oauth_provider_id": private_provider.id,
            }
        )
        self.assertEqual(
            new_user.role_id.id, self.ref("container_accessibility.role_administrator")
        )

    def test_new_user_without_private_provider(self):
        new_user = self.env["res.users"]._create_user_from_template(
            {"login": "someuser", "name": "Someuser 1"}
        )
        self.assertTrue(new_user.has_group("base.group_portal"))
        self.assertFalse(new_user.has_group("base.group_system"))
        self.assertFalse(new_user.has_group("container_accessibility.group_restricted"))
        self.assertEqual(
            new_user.role_id.id, self.ref("container_accessibility.role_guest")
        )

    def test_private_provider_without_role(self):
        with self.assertRaises(ValidationError):
            self.env["auth.oauth.provider"].create(
                {
                    "private": True,
                    "name": "Support oauth",
                    "auth_endpoint": "http://none",
                    "body": "Support Login",
                }
            )
