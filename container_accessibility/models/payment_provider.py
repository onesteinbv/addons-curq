from odoo import models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    def button_immediate_install(self):
        sudo_self = self
        if self.env.user.is_restricted_user() and self.env.user.has_group(
            "base.group_system"
        ):
            sudo_self = self.sudo()
        return super(PaymentProvider, sudo_self).button_immediate_install()
