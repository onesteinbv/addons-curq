from odoo import models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MailingMailing(models.Model):
    _inherit = "mailing.mailing"

    def _force_dedicated_server(self):
        """Check if dedicated server should be enforced"""
        self.ensure_one()
        sudo_config_parameter = self.env["ir.config_parameter"].sudo()
        force_dedicated_server = sudo_config_parameter.get_param(
            "mass_mailing_force_dedicated_server.enabled", "False"
        )
        if bool(
            safe_eval(force_dedicated_server)
        ):  # Allow also 0 and 1 and other falsy / truthy values
            param_mail_server_id = safe_eval(
                sudo_config_parameter.get_param("mass_mailing.mail_server_id", "0")
            )
            param_outgoing_mail_server = safe_eval(
                sudo_config_parameter.get_param(
                    "mass_mailing.outgoing_mail_server", "False"
                )
            )
            if not param_mail_server_id or not param_outgoing_mail_server:
                raise UserError(
                    self.env._("Please configure a dedicated outgoing server.")
                )
            if (
                not self.mail_server_id
            ):  # Forcing a mail_server_id is actually enough because mass_mailing.mail_server_id is only used as default value, checking the system parameters is for UX and preventing exploiting test emails
                raise UserError(
                    self.env._("Please select a mail server (in the Settings tab).")
                )

    def action_test(self):
        self._force_dedicated_server()
        return super().action_test()

    def action_put_in_queue(self):
        for mailing in self:
            mailing._force_dedicated_server()
        return super().action_put_in_queue()

    def action_schedule(self):
        self._force_dedicated_server()
        return super().action_put_in_queue()

    def action_send_mail(self, res_ids=None):
        # Prevents users to bypass the check if the state is set to in_queue manually by a rpc call
        for mailing in self:
            mailing._force_dedicated_server()
        return super().action_send_mail(res_ids=res_ids)
