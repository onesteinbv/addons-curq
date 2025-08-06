from odoo import api, models
from odoo.exceptions import AccessError


class IrCron(models.Model):
    _inherit = "ir.cron"

    def write(self, vals):
        res = super().write(vals)
        if not self.env.su and self.env.ref(
            "auditlog.model_auditlog_autovacuum"
        ) in self.mapped("model_id"):
            raise AccessError(self.env._("Access Denied"))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if not self.env.su and self.env.ref(
            "auditlog.model_auditlog_autovacuum"
        ) in self.mapped("model_id"):
            raise AccessError(self.env._("Access Denied"))
        return res

    def unlink(self):
        if not self.env.su and self.env.ref(
            "auditlog.model_auditlog_autovacuum"
        ) in self.mapped("model_id"):
            raise AccessError(self.env._("Access Denied"))
        return super().unlink()

    def method_direct_trigger(self):
        return super(
            IrCron, self.env.user.has_group("base.group_system") and self.sudo() or self
        ).method_direct_trigger()
