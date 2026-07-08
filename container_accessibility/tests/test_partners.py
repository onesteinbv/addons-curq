from odoo.addons.base.tests.common import BaseCommon


class TestPartners(BaseCommon):
    def test_partners_hidden(self):
        """
        Partners related to users outside of the
        container_accessibility.role_manager, container_accessibility.role_user, and container_accessibility.role_accountant roles
        should be hidden for these users.
        """
        manager_role = self.env.ref("container_accessibility.role_manager")
        administrator_role = self.env.ref("container_accessibility.role_administrator")
        user_role = self.env.ref("container_accessibility.role_user")

        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_user",
                "role_id": user_role.id,
            }
        )
        manager_user = self.env["res.users"].create(
            {
                "name": "Manager User",
                "login": "manager_user",
                "role_id": manager_role.id,
            }
        )
        administrator_user = self.env["res.users"].create(
            {
                "name": "Administrator User",
                "login": "administrator_user",
                "role_id": administrator_role.id,
            }
        )
        user_without_role = self.env["res.users"].create(
            {
                "name": "User Without Role",
                "login": "user_without_role",
                "role_id": None,
            }
        )

        # User with manager role should be able to see partners related to users with manager, accountant, or user role
        partners = self.env["res.partner"].with_user(manager_user).search([])
        self.assertIn(user.partner_id, partners)
        self.assertIn(manager_user.partner_id, partners)
        self.assertNotIn(administrator_user.partner_id, partners)
        self.assertNotIn(user_without_role.partner_id, partners)

        # User with administrator role should be able to see all partners
        partners = self.env["res.partner"].with_user(administrator_user).search([])
        self.assertIn(user.partner_id, partners)
        self.assertIn(manager_user.partner_id, partners)
        self.assertIn(administrator_user.partner_id, partners)
        self.assertIn(user_without_role.partner_id, partners)

        # User without role should be able to see all partners
        partners = (
            self.env["res.partner"]
            .with_user(self.env.ref("base.user_admin"))
            .search([])
        )

        self.assertIn(user.partner_id, partners)
        self.assertIn(manager_user.partner_id, partners)
        self.assertIn(administrator_user.partner_id, partners)
        self.assertIn(user_without_role.partner_id, partners)
