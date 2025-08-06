from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    updated_by_script = fields.Boolean(
        string="Updated by Script?",
        help="Whether this record has been updated by scripts/update_company.py",
    )
