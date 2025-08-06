from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def button_immediate_install(self):
        res = super().button_immediate_install()
        if self.env.context.get("onboarding_wizard", False):
            return {"type": "ir.actions.act_url", "url": "/web", "target": "self"}
        return res

    def button_immediate_uninstall(self):
        res = super().button_immediate_uninstall()
        if self.env.context.get("onboarding_wizard", False):
            return {"type": "ir.actions.act_url", "url": "/web", "target": "self"}
        return res
