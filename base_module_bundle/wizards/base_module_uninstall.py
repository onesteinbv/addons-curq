from odoo import api, fields, models


class ModuleUninstall(models.TransientModel):
    _inherit = "base.module.uninstall"

    is_bundle = fields.Boolean(compute="_compute_is_bundle")

    @api.depends("module_id")
    def _compute_is_bundle(self):
        for wizard in self:
            wizard.is_bundle = wizard.module_id.is_bundle

    @api.depends("is_bundle")
    def _compute_module_ids(self):
        pass
