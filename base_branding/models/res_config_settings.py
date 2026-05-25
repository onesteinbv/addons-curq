from lxml import etree

from odoo import api, models


class ResConfigSettings(models.TransientModel):
    """Curq branding for settings form."""

    _inherit = "res.config.settings"

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options=options)

        if "form" in res["views"]:
            xml_arch = etree.fromstring(res["views"]["form"]["arch"])

            # 1. Strip out the documentation attribute from <setting> tags
            for setting in xml_arch.xpath("//setting[@documentation]"):
                setting.attrib.pop("documentation", None)

            # 2. Find and completely remove <widget name="documentation_link"/> elements
            for widget in xml_arch.xpath("//widget[@name='documentation_link']"):
                widget.getparent().remove(widget)

            # Convert back to a string so we can perform a global text replacement
            arch_string = etree.tostring(xml_arch, encoding="utf-8").decode("utf-8")

            # 3. Globally replace "Odoo" with "PK"
            arch_string = arch_string.replace("Odoo", "Curq").replace("odoo", "curq")

            # Assign the modified architecture string back to the view definition
            res["views"]["form"]["arch"] = arch_string

        return res
