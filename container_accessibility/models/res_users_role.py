from odoo import api, models
from odoo.exceptions import AccessError


class ResUsersRole(models.Model):
    _name = "res.users.role"
    _inherit = ["res.users.role", "container.restrict.mixin"]

    @api.model_create_multi
    def create(self, vals_list):
        # base_user_role create method bypasses access rights checks and escalates privileges,
        # so we need to override it to add our own checks
        if self.env.user.is_restricted_user():
            raise AccessError(
                self.env._("Access denied to this model (res.users.role)")
            )
        return super(ResUsersRole, self).create(vals_list)

    def write(self, vals):
        if self.env.user.is_restricted_user():
            raise AccessError(
                self.env._("Access denied to this model (res.users.role)")
            )
        return super(ResUsersRole, self).write(vals)
