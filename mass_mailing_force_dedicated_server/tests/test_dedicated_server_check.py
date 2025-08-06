from odoo.exceptions import UserError

from odoo.addons.base.tests.common import BaseCommon


class TestDedicatedServerCheck(BaseCommon):
    def test_disabled(self):
        """Check if mass mailing still works if mass_mailing_force_dedicated_server.enabled is False"""
        self.env["ir.config_parameter"].set_param(
            "mass_mailing_force_dedicated_server.enabled", False
        )
        mailing = self.env["mailing.mailing"].create({"subject": "normal test"})
        mailing.action_test()
        mailing.action_put_in_queue()
        mailing.action_schedule()

        mailing_test_wizard = self.env["mailing.mailing.test"].create(
            {"mass_mailing_id": mailing.id}
        )
        mailing_test_wizard.send_mail_test()
        self.assertFalse(
            mailing.message_ids.filtered(
                lambda m: "Please configure a dedicated outgoing server" in m.body
                or "Please select a mail server" in m.body
            )
        )

    def test_enabled_not_configured(self):
        """Check if mass mailing is failing when mass_mailing_force_dedicated_server.enabled is True and dedicated server is not configured"""
        config_parameter = self.env["ir.config_parameter"]
        config_parameter.set_param("mass_mailing_force_dedicated_server.enabled", True)
        config_parameter.set_param("mass_mailing.mail_server_id", "0")
        config_parameter.set_param("mass_mailing.outgoing_mail_server", "False")

        mailing = self.env["mailing.mailing"].create({"subject": "normal test"})
        with self.assertRaisesRegex(
            UserError, "Please configure a dedicated outgoing server"
        ):
            mailing.action_test()
        with self.assertRaisesRegex(
            UserError, "Please configure a dedicated outgoing server"
        ):
            mailing.action_put_in_queue()
        with self.assertRaisesRegex(
            UserError, "Please configure a dedicated outgoing server"
        ):
            mailing.action_schedule()

        mailing_test_wizard = self.env["mailing.mailing.test"].create(
            {"mass_mailing_id": mailing.id}
        )
        mailing_test_wizard.send_mail_test()
        self.assertTrue(
            mailing.message_ids.filtered(
                lambda m: "Please configure a dedicated outgoing server" in m.body
            )
        )

    def test_enabled_configured(self):
        """Check if mass mailing is failing when mass_mailing_force_dedicated_server.enabled is True and dedicated server is configured"""
        mail_server = self.env["ir.mail_server"].create(
            {"name": "mail server", "smtp_host": "localhost"}
        )
        config_parameter = self.env["ir.config_parameter"]
        config_parameter.set_param("mass_mailing_force_dedicated_server.enabled", True)
        config_parameter.set_param("mass_mailing.mail_server_id", mail_server.id)
        config_parameter.set_param("mass_mailing.outgoing_mail_server", "True")

        mailing = self.env["mailing.mailing"].create({"subject": "normal test"})
        mailing.action_test()
        mailing.action_put_in_queue()
        mailing.action_schedule()

        mailing.mail_server_id = False
        with self.assertRaisesRegex(UserError, "Please select a mail server"):
            mailing.action_test()
        with self.assertRaisesRegex(UserError, "Please select a mail server"):
            mailing.action_put_in_queue()
        with self.assertRaisesRegex(UserError, "Please select a mail server"):
            mailing.action_schedule()

        mailing_test_wizard = self.env["mailing.mailing.test"].create(
            {"mass_mailing_id": mailing.id}
        )
        mailing_test_wizard.send_mail_test()  # raise_exception is False and log is too assertLogs("INFO") is too generic
        self.assertTrue(
            mailing.message_ids.filtered(
                lambda m: "Please select a mail server" in m.body
            )
        )
