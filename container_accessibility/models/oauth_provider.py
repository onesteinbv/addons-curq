from odoo import fields, models
from odoo.exceptions import AccessError


class OauthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    private = fields.Boolean()
    template_user_id = fields.Many2one(comodel_name="res.users", ondelete="restrict")
    group_ids = fields.Many2many(comodel_name="res.groups")

    def write(self, vals):
        if (
            self.env.user.is_restricted_user() and vals.get("private")
        ):  # The record rule doesn't care if the record was non-private before the write.
            raise AccessError(self.env._("Access denied"))
        return super().write(vals)
