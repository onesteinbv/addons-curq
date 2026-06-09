from odoo import fields, models


class ResUsersRole(models.Model):
    _inherit = "res.users.role"

    implied_by_text = fields.Text(
        string="Implied by",
        compute="_compute_implied_by_text",
        inverse="_inverse_implied_by_text",
        help="Textual representation of the groups of this role. Seperated by new lines.",
    )

    def _compute_implied_by_text(self):
        for role in self:
            pass

    def _inverse_implied_by_text(self):
        for role in self:
            pass
