from odoo import api, models
from odoo.exceptions import AccessError


class AuditlogLogLine(models.Model):
    _inherit = "auditlog.log.line"

    def write(self, vals):
        if not self.env.su:
            raise AccessError(self.env._("Access denied"))
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su:
            raise AccessError(self.env._("Access denied"))
        return super().create(vals_list)

    def unlink(self):
        if not self.env.su:
            raise AccessError(self.env._("Access denied"))
        return super().unlink()
