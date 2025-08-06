from odoo import fields, models


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    private = fields.Boolean(string="Is private server")
