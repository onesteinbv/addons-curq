from odoo import api, models


class ModuleUninstall(models.TransientModel):
    _inherit = "base.module.uninstall"

    def _get_modules(self):
        modules = super()._get_modules()
        if not self.module_id.is_bundle:
            return modules
        modules += self.module_id._get_modules_to_uninstall_for_bundle()
        return modules

    @api.depends("module_id.is_bundle")
    def _compute_module_ids(self):
        return super()._compute_module_ids()
