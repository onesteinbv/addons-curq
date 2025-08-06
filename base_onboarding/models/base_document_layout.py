from odoo import fields, models


class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"

    onboarding = fields.Boolean(
        default=lambda self: self.env.context.get("active_model")
        == "base.onboarding.wizard"
    )

    def document_layout_save(self):
        res = super().document_layout_save()
        if self.env.context.get("active_model") == "base.onboarding.wizard":
            wizard = self.env["base.onboarding.wizard"].search(
                [("id", "=", self.env.context.get("active_id"))]
            )
            res = wizard._reopen_self()
        return res
