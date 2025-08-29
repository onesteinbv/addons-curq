from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    currency_rates_autoupdate = fields.Boolean(
        default=False,
    )
