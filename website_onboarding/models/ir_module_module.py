from odoo import api, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def _fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        if (
            view_type == "kanban"
            and self.env.context.get("active_model") == "base.onboarding.wizard"
        ):
            view_id = self.env.ref("website.theme_view_kanban").id
        return super()._fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

    def button_choose_theme(self):
        res = super().button_choose_theme()
        if self.env.context.get("active_model") == "base.onboarding.wizard":
            wizard = self.env["base.onboarding.wizard"].search(
                [("id", "=", self.env.context.get("active_id"))]
            )
            if wizard.state == "theme":
                wizard.open_next()
            res = wizard._reopen_self()
        return res
