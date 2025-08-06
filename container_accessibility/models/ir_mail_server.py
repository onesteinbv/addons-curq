from odoo import fields, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    private = fields.Boolean(string="Is private server")
