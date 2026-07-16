from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError


class OauthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    private = fields.Boolean()
    role_id = fields.Many2one(comodel_name="res.users.role")

    @api.constrains("role_id", "private")
    def _constrain_private(self):
        if self.filtered(lambda r: r.private and not r.role_id):
            raise ValidationError(
                self.env._("Private OAuth providers must have a role.")
            )

    def write(self, vals):
        if (
            self.env.user.is_restricted_user() and vals.get("private")
        ):  # The record rule doesn't care if the record was non-private before the write.
            raise AccessError(self.env._("Access denied"))
        return super().write(vals)
