from odoo.addons.base.tests.common import BaseCommon


class TestOauth(BaseCommon):
    def test_new_user_without_groups(self):
        private_provider = self.env["auth.oauth.provider"].create(
            {
                "private": True,
                "name": "Support oauth",
                "template_user_id": self.env.ref("base.user_admin").id,
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
        self.assertTrue(new_user.has_group("base.group_system"))

    def test_new_user_with_extra_groups(self):
        private_provider = self.env["auth.oauth.provider"].create(
            {
                "private": True,
                "name": "Reseller oauth",
                "template_user_id": self.env.ref("base.user_admin").id,
                "group_ids": self.env.ref(
                    "container_accessibility.group_restricted"
                ).ids,
                "auth_endpoint": "http://none",
                "body": "Reseller Login",
            }
        )
        new_user = self.env["res.users"]._create_user_from_template(
            {
                "login": "reseller1",
                "name": "Reseller 1",
                "oauth_provider_id": private_provider.id,
            }
        )
        self.assertTrue(new_user.has_group("base.group_system"))
        self.assertTrue(new_user.has_group("container_accessibility.group_restricted"))

    def test_new_user_without_private_provider(self):
        new_user = self.env["res.users"]._create_user_from_template(
            {"login": "reseller1", "name": "Reseller 1"}
        )
        self.assertTrue(new_user.has_group("base.group_portal"))
        self.assertFalse(new_user.has_group("base.group_system"))
        self.assertFalse(new_user.has_group("container_accessibility.group_restricted"))
