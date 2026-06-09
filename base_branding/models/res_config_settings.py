from lxml import etree

from odoo import api, models


class ResConfigSettings(models.TransientModel):
    """CURQ branding for settings form."""

    _inherit = "res.config.settings"

    def _get_selectors_to_brand(self):
        """
        Returns a list of selectors (xpath expressions) to brand.
        """
        return ["//title", "//label", "//field", "//strong", "//button", "//setting"]

    def _get_attributes_to_brand(self):
        """
        Returns a list of attributes to brand.
        """
        return [
            "string",
            "name",
            "placeholder",
            "confirm",
            "title",
            "help",
        ]

    def _brand_text(self, text):
        """
        Replaces occurrences of "Odoo" or "odoo" in the given text with "CURQ".
        """

        replacements = [
            ("https://www.odoo.com", "https://curq.nl"),
            ("Odoo", "CURQ"),
            ("odoo", "CURQ"),
        ]

        if not text:
            return text
        for old, new in replacements:
            text = text.replace(old, new)
        return text

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options=options)

        if "form" not in res["views"]:
            return res

        xml_arch = etree.fromstring(res["views"]["form"]["arch"])

        # Strip out the documentation attribute from <setting> tags
        for setting in xml_arch.xpath("//setting[@documentation]"):
            setting.attrib.pop("documentation", None)

        # Find and completely remove <widget name="documentation_link"/> elements
        for widget in xml_arch.xpath("//widget[@name='documentation_link']"):
            widget.getparent().remove(widget)

        # Brand XML
        selectors_to_brand = self._get_selectors_to_brand()
        for selector in selectors_to_brand:
            for element in xml_arch.xpath(selector):
                # Remove any occurrence of "Odoo" or "odoo" in the text content of the element
                if element.text:
                    element.text = self._brand_text(element.text)

                # If the element has attributes, check if any of them are
                # in the list of attributes to brand and replace "Odoo" or "odoo" in their values
                if not element.attrib:
                    continue

                attributes_to_brand = self._get_attributes_to_brand()
                for attr, val in element.attrib.items():
                    if attr not in attributes_to_brand:
                        continue
                    element.attrib[attr] = self._brand_text(val)

        # Assign the modified architecture string back to the view definition
        res["views"]["form"]["arch"] = etree.tostring(
            xml_arch, encoding="utf-8"
        ).decode("utf-8")
        return res
