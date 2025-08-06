from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_auth_oauth = fields.Boolean(readonly=True)

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        """Hide all module options"""
        arch, view = super()._get_view(view_id, view_type, **options)
        if self.env.user.is_restricted_user() and view_type == "form":
            nodes = arch.xpath(
                "//field[starts-with(@name, 'module_') and not(@invisible)]"
            )
            for node in nodes:
                element = node
                setting_box = None
                while setting_box is None:
                    element = element.getparent()
                    if element is None:
                        setting_box = node.getparent()
                        break
                    if "o_setting_box" in element.attrib.get("class", ""):
                        setting_box = element
                if setting_box.getparent() is not None:
                    setting_box.getparent().remove(setting_box)
                else:
                    setting_box.clear()

        return arch, view

    def execute(self):
        sudo_self = self
        if self.env.user.is_restricted_user() and self.env.user.has_group(
            "base.group_system"
        ):
            sudo_self = self.sudo()
        return super(ResConfigSettings, sudo_self).execute()
