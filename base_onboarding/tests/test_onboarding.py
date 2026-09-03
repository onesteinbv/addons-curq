from unittest.mock import patch

from odoo.tests import common

from odoo.addons.base.models.ir_module import Module


class TestOnboarding(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard_model = cls.env["base.onboarding.wizard"]
        cls.layout_model = cls.env["base.document.layout"]
        cls.onboarding_group = cls.env.ref("base_onboarding.onboarding_group")
        cls.user_admin = cls.env.ref("base.user_admin")

    def test_onboarding_wizard_workflow(self):
        """Test wizard steps navigation and state transitions."""
        wizard = self.wizard_model.with_user(self.user_admin).create({})
        self.assertEqual(wizard.state, "start")
        self.assertEqual(wizard.company_id, self.env.company)
        self.assertFalse(wizard.allow_back)
        self.assertTrue(wizard.module_ids)

        action = wizard.open_next()
        self.assertEqual(wizard.state, "company_info")
        self.assertTrue(wizard.allow_back)
        self.assertEqual(action.get("name"), "Welcome to CURQ")

        wizard.write(
            {
                "company_vat": "NL123456789B01",
                "company_registry": "12345678",
                "company_phone": "+31123456789",
                "company_email": "info@example.com",
                "company_website": "https://example.com",
            }
        )
        self.assertEqual(wizard.company_id.vat, "NL123456789B01")
        self.assertEqual(wizard.company_id.company_registry, "12345678")
        self.assertEqual(wizard.company_id.phone, "+31123456789")
        self.assertEqual(wizard.company_id.email, "info@example.com")
        self.assertEqual(wizard.company_id.website, "https://example.com")
        wizard.open_next()
        self.assertEqual(wizard.state, "mailing")

        # Configure mail servers
        mail_server = self.env["ir.mail_server"].create(
            {"name": "Outgoing Test", "smtp_host": "smtp.example.com"}
        )
        fetchmail_server = self.env["fetchmail.server"].create(
            {
                "name": "Incoming Test",
                "server_type": "imap",
                "server": "imap.example.com",
            }
        )
        wizard.write(
            {
                "ir_mail_server_id": mail_server.id,
                "fetchmail_server_id": fetchmail_server.id,
            }
        )
        self.assertEqual(wizard.ir_mail_server_id, mail_server)
        self.assertEqual(wizard.fetchmail_server_id, fetchmail_server)

        # Ensure admin user is in onboarding group before entering final
        self.onboarding_group.sudo().write({"users": [(4, self.user_admin.id)]})
        self.assertIn(self.user_admin, self.onboarding_group.users)

        action = wizard.open_next()
        self.assertEqual(wizard.state, "final")
        self.assertEqual(action.get("name"), "Welcome to CURQ")
        self.assertNotIn(self.user_admin, self.onboarding_group.users)

    def test_onboarding_wizard_skip_to_end(self):
        """Test skip_to_end directly transitions to final state."""
        self.onboarding_group.sudo().write({"users": [(4, self.user_admin.id)]})
        self.assertIn(self.user_admin, self.onboarding_group.users)

        wizard = self.wizard_model.with_user(self.user_admin).create({})
        action = wizard.skip_to_end()
        self.assertEqual(wizard.state, "final")
        self.assertEqual(action.get("name"), "Welcome to CURQ")
        self.assertNotIn(self.user_admin, self.onboarding_group.users)

    def test_base_document_layout(self):
        """Test onboarding field and document_layout_save on base.document.layout."""
        layout = self.layout_model.new()
        self.assertFalse(layout.onboarding)
        wizard = self.wizard_model.create({})
        ctx = {"active_model": "base.onboarding.wizard", "active_id": wizard.id}
        layout_onboarding = self.layout_model.with_context(**ctx).new()
        self.assertTrue(layout_onboarding.onboarding)

        # document_layout_save with wizard context reopens wizard
        res = layout_onboarding.document_layout_save()
        self.assertIsInstance(res, dict)
        self.assertEqual(res.get("name"), "Welcome to CURQ")

        # document_layout_save without wizard context behaves normally
        layout_normal = self.layout_model.new()
        res_normal = layout_normal.document_layout_save()
        self.assertNotEqual(res_normal.get("name"), "Welcome to CURQ")

    def test_ir_module_module_onboarding_context(self):
        """Test immediate install and uninstall redirects when in onboarding wizard."""
        module = self.env["ir.module.module"].search(
            [("name", "=", "base_onboarding")], limit=1
        )
        self.assertTrue(module)

        expected_url_action = {
            "type": "ir.actions.act_url",
            "url": "/web",
            "target": "self",
        }

        with patch.object(
            Module,
            "button_immediate_install",
            return_value={"type": "standard_install"},
        ):
            res = module.button_immediate_install()
            self.assertEqual(res, {"type": "standard_install"})
            res = module.with_context(onboarding_wizard=True).button_immediate_install()
            self.assertEqual(res, expected_url_action)

        with patch.object(
            Module,
            "button_immediate_uninstall",
            return_value={"type": "standard_uninstall"},
        ):
            res = module.button_immediate_uninstall()
            self.assertEqual(res, {"type": "standard_uninstall"})
            res = module.with_context(
                onboarding_wizard=True
            ).button_immediate_uninstall()
            self.assertEqual(res, expected_url_action)
