from lxml import etree

from odoo import api, models


class ResConfigSettings(models.TransientModel):
    """CURQ branding for settings form."""

    _inherit = "res.config.settings"

    def _get_selectors_to_debrand(self):
        """
        Returns a list of selectors (attribute names) to debrand.
        """
        return ["string", "help", "title", "placeholder", "confirm"]

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

            # 3. Debrand XML
            selectors_to_debrand = self._get_selectors_to_debrand()
            for element in xml_arch.iter():
                if element.text and ("Odoo" in element.text or "odoo" in element.text):
                    element.text = element.text.replace("Odoo", "CURQ").replace(
                        "odoo", "CURQ"
                    )
                if element.tail and ("Odoo" in element.tail or "odoo" in element.tail):
                    element.tail = element.tail.replace("Odoo", "CURQ").replace(
                        "odoo", "CURQ"
                    )
                if element.attrib:
                    for attr, val in element.attrib.items():
                        if attr in selectors_to_debrand and (
                            "Odoo" in val or "odoo" in val
                        ):
                            element.attrib[attr] = val.replace("Odoo", "CURQ").replace(
                                "odoo", "CURQ"
                            )

            # Assign the modified architecture string back to the view definition
            res["views"]["form"]["arch"] = etree.tostring(
                xml_arch, encoding="utf-8"
            ).decode("utf-8")

        return res
