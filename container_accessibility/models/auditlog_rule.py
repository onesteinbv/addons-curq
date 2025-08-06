from odoo import api, fields, models
from odoo.exceptions import AccessError


class AuditlogRule(models.Model):
    _inherit = "auditlog.rule"

    private = fields.Boolean()

    def write(self, vals):
        res = super().write(vals)
        if not self.env.su and self.filtered(lambda r: r.private):
            raise AccessError(self.env._("Restricted to edit required auditlog rules"))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if not self.env.su and self.filtered(lambda r: r.private):
            raise AccessError(self.env._("Restricted to create required auditlog rule"))
        return res

    def unlink(self):
        if not self.env.su and self.filtered(lambda r: r.private):
            raise AccessError(
                self.env._("Restricted to delete required auditlog rules")
            )
        return super().unlink()

    def create_logs(
        self,
        uid,
        res_model,
        res_ids,
        method,
        old_values=None,
        new_values=None,
        additional_log_values=None,
    ):
        return super(AuditlogRule, self.sudo()).create_logs(
            uid,
            res_model,
            res_ids,
            method,
            old_values=old_values,
            new_values=new_values,
            additional_log_values=additional_log_values,
        )
