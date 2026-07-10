from odoo.tests.common import TransactionCase


class TestAllowedConfigSettings(TransactionCase):
    def test_clean_parse(self):
        roles = self.env["res.users.role"].search(
            [("allowed_config_settings", "!=", False)]
        )
        for role in roles:
            allowed_config_settings = role._parse_allowed_config_settings()

            # Must be non-empty strings
            self.assertTrue(
                all(allowed_config_settings),
                "Allowed config settings should be non-empty strings",
            )

            # Should not have any leading or trailing whitespace
            self.assertTrue(
                all(s == s.strip() for s in allowed_config_settings),
                "Allowed config settings should not have leading or trailing whitespace",
            )

    def test_execute_module_installation_uninstallation(self):
        """Test that the execute method of res.config.settings doesn't install or uninstall modules."""
        administrator = self.env["res.users"].create(
            {
                "name": "Administrator",
                "login": "new_admin_user",
                "role_id": self.ref("container_accessibility.role_administrator"),
            }
        )
        not_installed_module = self.env.ref("base.module_auth_ldap")
        installed_module = self.env.ref("base.module_auth_oauth")
        self.assertEqual(not_installed_module.state, "uninstalled")
        self.assertEqual(installed_module.state, "installed")

        settings = self.env["res.config.settings"].with_user(administrator).create({})
        settings.module_auth_ldap = True  # This would normally install the module
        settings.module_auth_oauth = False  # This would normally uninstall the module
        settings.execute()
        self.assertEqual(not_installed_module.state, "uninstalled")
        self.assertEqual(installed_module.state, "installed")

    def test_execute_disallowed_setting(self):
        manager = self.env["res.users"].create(
            {
                "name": "Manager",
                "login": "new_manager_user",
                "role_id": self.ref("container_accessibility.role_manager"),
            }
        )
        administrator = self.env["res.users"].create(
            {
                "name": "Administrator",
                "login": "new_admin_user",
                "role_id": self.ref("container_accessibility.role_administrator"),
            }
        )
        real_admin = self.env.ref("base.user_admin")

        group_user = self.env.ref("base.group_user")
        group_multi_currency = self.env.ref("base.group_multi_currency")

        # Disallowed
        self.assertNotIn(group_multi_currency, group_user.implied_ids)
        settings = self.env["res.config.settings"].with_user(manager).create({})
        settings.group_multi_currency = (
            True  # This would normally add the group to the internal user group
        )
        settings.execute()
        self.assertNotIn(group_multi_currency, group_user.implied_ids)

        # Allowed
        settings = self.env["res.config.settings"].with_user(real_admin).create({})
        settings.group_multi_currency = True
        settings.execute()
        self.assertIn(group_multi_currency, group_user.implied_ids)

        # Disallowed
        settings = self.env["res.config.settings"].with_user(manager).create({})
        settings.group_multi_currency = (
            False  # This would normally remove the group from the internal user group
        )
        settings.execute()
        self.assertIn(group_multi_currency, group_user.implied_ids)

        # Allowed admin role
        settings = self.env["res.config.settings"].with_user(administrator).create({})
        settings.group_multi_currency = False
        settings.execute()
        self.assertNotIn(group_multi_currency, group_user.implied_ids)
