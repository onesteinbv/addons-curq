from odoo import conf, fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    is_bundle = fields.Boolean(
        help="A bundle purges dependencies on uninstallation of this module",
        compute="_compute_is_bundle",
    )  # Can't be stored

    def _compute_is_bundle(self):
        for module in self:
            module_info = self.get_module_info(module.name)
            module.is_bundle = module_info.get("bundle", False)

    def button_uninstall(self):
        """
        Uninstall upstream modules but only if they're not in another bundle modules dependency
        """
        modules = self.search([("state", "=", "installed")])
        bundle_modules = modules.filtered(lambda m: m.is_bundle)
        for to_uninstall in self:
            if to_uninstall not in bundle_modules:
                continue

            other_bundle_modules = bundle_modules.filtered(
                lambda m: m.id != to_uninstall.id
            )
            modules_to_keep = self.env["ir.module.module"].search(
                [("name", "in", conf.server_wide_modules)]
            )
            modules_to_keep += other_bundle_modules.upstream_dependencies(
                exclude_states=("uninstalled",)
            )
            modules_to_keep = set(modules_to_keep.mapped("name"))

            modules_to_remove = to_uninstall.upstream_dependencies(
                exclude_states=("uninstalled",)
            )
            modules_to_remove = modules_to_remove.filtered(
                lambda d: d.name not in modules_to_keep
            )
            return modules_to_remove.button_uninstall()

        return super().button_uninstall()
