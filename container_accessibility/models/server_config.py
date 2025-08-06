from odoo import api, models


class ServerConfiguration(models.TransientModel):  # We don't want this feature
    _inherit = "server.config"

    @api.model
    def default_get(self, fields_list):
        super().default_get(fields_list)
        return {}
