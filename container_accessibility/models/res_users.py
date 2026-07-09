from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config
from odoo.tools.misc import ustr

from odoo.addons.auth_signup.models.res_partner import SignupError


class ResUsers(models.Model):
    _inherit = "res.users"

    # Simplified role field without the possibility to have multiple roles
    role_id = fields.Many2one(
        comodel_name="res.users.role",
        inverse="_inverse_role_id",
        groups="base.group_erp_manager",
    )
    role_comment = fields.Text(
        related="role_id.comment", readonly=True, groups="base.group_erp_manager"
    )

    def _inverse_role_id(self):
        for user in self:
            active_role = user.role_line_ids.filtered(
                lambda r: r.role_id == user.role_id and r.is_enabled
            )
            if active_role:
                continue
            ops = [Command.clear()]
            if user.role_id:
                ops.append(Command.create({"role_id": user.role_id.id}))
            user.role_line_ids = ops

    @api.model
    def _get_user_limit(self):
        return int(config.get("user_limit", "0"))

    @api.model
    def _get_limit_included_roles(self):
        return (
            self.env.ref("container_accessibility.role_manager")
            + self.env.ref("container_accessibility.role_user")
            + self.env.ref("container_accessibility.role_accountant")
        )

    @api.model
    def _get_limit_included_user_count(self):
        roles = self._get_limit_included_roles()
        count = self.search_count([("role_id", "in", roles.ids)])
        return count

    def is_restricted_user(self):
        self.ensure_one()
        return self.sudo().has_group("container_accessibility.group_restricted")

    def write(self, vals):
        is_restricted = self.env.user.is_restricted_user()
        if is_restricted and "role_id" in vals and not vals.get("role_id"):
            raise ValidationError(
                _(
                    "Users must have a role assigned. Please assign a role to the user and try again."
                )
            )
        # Check if the user limit is exceeded when changing the role of a user
        if "role_id" in vals:
            user_limit = self._get_user_limit()
            if user_limit:
                included_roles = self._get_limit_included_roles()
                current_count = self._get_limit_included_user_count() - len(
                    self.filtered(lambda u: u.role_id in included_roles)
                )
                changing_to_included_role = vals.get("role_id") in included_roles.ids
                if changing_to_included_role and current_count + len(self) > user_limit:
                    raise ValidationError(_("User limit exceeded."))
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        is_restricted = self.env.user.is_restricted_user()
        role_ids = [vals.get("role_id") for vals in vals_list]
        if is_restricted and any(not role_id for role_id in role_ids):
            raise ValidationError(
                _(
                    "Users must have a role assigned. Please assign a role to the user and try again."
                )
            )

        # Check if the user limit is exceeded when creating new users
        user_limit = self._get_user_limit()
        if user_limit:
            included_roles = self._get_limit_included_roles()
            current_count = self._get_limit_included_user_count()
            creating_included_role = any(
                role_id in included_roles.ids for role_id in role_ids
            )
            if creating_included_role and current_count + len(vals_list) > user_limit:
                raise ValidationError(_("User limit exceeded."))

        return super().create(vals_list)

    def _create_user_from_template(self, values):
        if values.get("oauth_provider_id", False):
            provider_record = (
                self.env["auth.oauth.provider"]
                .sudo()
                .browse(values["oauth_provider_id"])
            )
            if not provider_record.private:
                guest_role = self.env.ref("container_accessibility.role_guest")
                values["role_id"] = guest_role.id
                return super()._create_user_from_template(values)

            role = provider_record.role_id or self.env.ref(
                "container_accessibility.role_guest"
            )
            template_user = self.env.ref("base.default_user")
            if not values.get("login"):
                raise ValueError(self.env._("Signup: no login given for new user"))
            if not values.get("partner_id") and not values.get("name"):
                raise ValueError(
                    self.env._("Signup: no name or partner given for new user")
                )
            values["active"] = True
            values["role_id"] = role.id
            try:
                with self.env.cr.savepoint():
                    new_user = template_user.with_context(no_reset_password=True).copy(
                        values
                    )
                    return new_user
            except Exception as e:
                raise SignupError(ustr(e)) from e
        guest_role = self.env.ref("container_accessibility.role_guest")
        values["role_id"] = guest_role.id
        return super()._create_user_from_template(values)

    @api.model
    def _signup_create_user(self, values):
        if values.get("oauth_provider_id", False):
            provider_record = (
                self.env["auth.oauth.provider"]
                .sudo()
                .browse(values["oauth_provider_id"])
            )
            if provider_record.private:
                return self._create_user_from_template(values)
        guest_role = self.env.ref("container_accessibility.role_guest")
        values["role_id"] = guest_role.id
        return super()._signup_create_user(values)
