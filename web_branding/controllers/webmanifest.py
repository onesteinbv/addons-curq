from odoo.http import request

from odoo.addons.web.controllers.webmanifest import WebManifest


class WebManifestBranded(WebManifest):
    def _get_webmanifest(self):
        manifest = super()._get_webmanifest()
        manifest["name"] = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("web.web_app_name", "CURQ")
        )
        manifest["background_color"] = "#FFC03D"
        manifest["theme_color"] = "#1C355E"

        icon_sizes = ["192x192", "512x512"]
        manifest["icons"] = [
            {
                "src": "/web_branding/static/img/icon.svg",
                "sizes": "any",
                "type": "image/svg+xml",
            }
        ] + [
            {
                "src": "/web_branding/static/img/icon-%s.png" % size,
                "sizes": size,
                "type": "image/png",
            }
            for size in icon_sizes
        ]
        return manifest
