from odoo import conf, fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    purge_depends = fields.Boolean(
        help="Purge dependencies on uninstallation of this module",
        compute="_compute_purge_depends",
    )  # Can't be stored

    def _compute_purge_depends(self):
        for module in self:
            module_info = self.get_module_info(module.name)
            module.purge_depends = module_info.get("purge_depends", False)

    def button_uninstall(self):
        """
        Uninstall upstream modules but only if they're not in another `purge_depends` modules dependency
        """
        modules = self.search([("state", "=", "installed")])
        purge_modules = modules.filtered(lambda m: m.purge_depends)
        for to_uninstall in self:
            if to_uninstall not in purge_modules:
                continue

            other_purge_modules = purge_modules.filtered(
                lambda m: m.id != to_uninstall.id
            )
            modules_to_keep = self.env["ir.module.module"].search(
                [("name", "in", conf.server_wide_modules)]
            )
            for other_purge_module in other_purge_modules:
                modules_to_keep += other_purge_module.upstream_dependencies(
                    exclude_states=("uninstalled",)
                )
            modules_to_keep = modules_to_keep.mapped("name")

            modules_to_remove = to_uninstall.upstream_dependencies(
                exclude_states=("uninstalled",)
            )
            modules_to_remove = modules_to_remove.filtered(
                lambda d: d.name not in modules_to_keep
            )
            return modules_to_remove.button_uninstall()

        return super().button_uninstall()
