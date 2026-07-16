from odoo import api, fields, models
from odoo.exceptions import AccessError


class ResUsersRole(models.Model):
    _name = "res.users.role"
    _inherit = ["res.users.role", "container.restrict.mixin"]

    allowed_config_settings = fields.Text()

    def _parse_allowed_config_settings(self):
        """Parses the allowed config settings for this role."""
        self.ensure_one()
        if self.allowed_config_settings:
            stripped = [s.strip() for s in self.allowed_config_settings.split("\n")]
            cleaned = [s for s in stripped if s]  # Remove empty strings
            return cleaned
        return []

    def get_allowed_config_settings(self):
        """Returns the allowed config settings for this role."""
        allowed_config_settings = self._parse_allowed_config_settings()
        domain = [("model", "=", "res.config.settings")]
        if allowed_config_settings:
            domain.append(("name", "in", allowed_config_settings))
        fields = self.env["ir.model.fields"].search(domain)
        return fields.mapped("name")

    def get_disallowed_config_settings(self):
        """Returns the disallowed config settings for this role."""
        allowed_config_settings = self._parse_allowed_config_settings()
        if not allowed_config_settings:
            return []
        standard_fields = ["id", "create_uid", "create_date", "write_uid", "write_date"]
        disallowed_fields = self.env["ir.model.fields"].search(
            [
                ("model", "=", "res.config.settings"),
                ("name", "not in", allowed_config_settings + standard_fields),
            ]
        )
        return disallowed_fields.mapped("name")

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
