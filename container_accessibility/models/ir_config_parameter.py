from odoo import _, models
from odoo.exceptions import AccessError


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def write(self, values):
        if self.filtered(lambda p: p.key == "base.template_portal_user_id"):
            raise AccessError(
                _(
                    "Access denied to change system parameter base.template_portal_user_id"
                )
            )
        return super().write(values)
