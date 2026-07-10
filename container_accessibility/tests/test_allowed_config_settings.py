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
