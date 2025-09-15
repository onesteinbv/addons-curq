from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    mandate_visible = fields.Boolean(
        compute="_compute_mandate_visible",
    )

    @api.depends("mandate_id", "move_type")
    def _compute_mandate_visible(self):
        has_group = self.env.user.has_group(
            "account_banking_pain_base.group_pain_multiple_identifier"
        )
        for move in self:
            if move.move_type not in (
                "out_invoice",
                "out_refund",
                "in_invoice",
                "in_refund",
            ):
                move.mandate_visible = False
            elif not has_group and move.move_type in ("out_invoice", "out_refund"):
                move.mandate_visible = False
            else:
                move.mandate_visible = True
