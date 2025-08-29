from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_mail_template(self):
        """
        :return: the correct mail template based on the current move type
        """
        return (
            super()._get_mail_template()
            if all(move.move_type == "out_refund" for move in self)
            else self.env.ref("account_configuration.email_template_send_invoice")
        )
