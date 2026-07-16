from odoo import api, fields, models

SENTINEL = object()


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_auth_oauth = fields.Boolean(readonly=True)

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type="form", **options):
        cache_key = super()._get_view_cache_key(
            view_id=view_id, view_type=view_type, **options
        )
        if self.env.user.is_restricted_user():
            cache_key += (self.env.user.role_id.id,)
        return cache_key

    def _remove_empty_upstream(self, element):
        """Recursively remove empty parent elements up the tree."""
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)
            remaining_children = parent.xpath(".//field")
            if not remaining_children:
                self._remove_empty_upstream(parent)

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        """Hide all disallowed config settings for restricted users."""
        arch, view = super()._get_view(view_id, view_type, **options)
        if self.env.user.is_restricted_user() and view_type == "form":
            role = self.env.user.role_id
            disallowed_config_settings = role.get_disallowed_config_settings()
            for field_name in disallowed_config_settings:
                nodes = arch.xpath("//field[@name='%s']" % field_name)
                for node in nodes:
                    element = node
                    # Find the parent setting box of the field
                    setting_box = None
                    while setting_box is None:
                        element = element.getparent()
                        if element is None:
                            break
                        if (
                            "o_setting_box" in element.attrib.get("class", "")
                            or element.tag == "setting"
                        ):
                            setting_box = element
                    if setting_box is None:
                        continue
                    self._remove_empty_upstream(setting_box)

        return arch, view

    @api.model
    def default_get(self, fields):
        """Override default_get to bypass the allowed config settings filter to prevent warnings"""
        return super(
            ResConfigSettings, self.with_context(bypass_allowed_fields=SENTINEL)
        ).default_get(fields)

    def _get_classified_fields(self, fnames=None):
        """Remove all disallowed config settings for restricted users."""
        if (
            self.env.user.is_restricted_user()
            and self.env.context.get("bypass_allowed_fields") is not SENTINEL
        ):
            role = self.env.user.role_id
            allowed_config_settings = role.get_allowed_config_settings()
            if not allowed_config_settings:
                return super()._get_classified_fields(fnames=fnames)
            classified = super()._get_classified_fields(fnames=fnames)
            for key in ("default", "group", "config"):
                classified[key] = [
                    field
                    for field in classified[key]
                    if field[0] in allowed_config_settings
                ]

            # Other fields are not a tuple like the other classified fields
            classified["other"] = [
                field
                for field in classified["other"]
                if field in allowed_config_settings
            ]

            # Disallow module config settings for restricted users, classified["module"] is a recordset of ir.module.module records
            allowed_modules = [
                field_name[7:]
                for field_name in allowed_config_settings
                if field_name.startswith("module_")
            ]
            classified["module"] = classified["module"].filtered(
                lambda m: m.name in allowed_modules
            )
            return classified
        return super()._get_classified_fields(fnames=fnames)

    def execute(self):
        sudo_self = self
        if self.env.user.is_restricted_user() and self.env.user.has_group(
            "base.group_system"
        ):
            sudo_self = self.sudo()
        return super(ResConfigSettings, sudo_self).execute()

    @api.depends("company_id")
    def _compute_active_user_count(self):
        res = super()._compute_active_user_count()
        if self.env.user.is_restricted_user():
            active_user_count = self.env["res.users"]._get_limit_included_user_count()
            for record in self:
                record.active_user_count = active_user_count
        return res
