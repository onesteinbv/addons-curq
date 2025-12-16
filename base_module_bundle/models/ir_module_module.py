from odoo import api, conf, fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    is_bundle = fields.Boolean(
        help="A bundle purges dependencies on uninstallation of this module",
        compute="_compute_is_bundle",
    )  # Can't be stored
    module_type = fields.Selection(
        selection_add=[("bundles", "Bundles")], ondelete={"bundles": "set default"}
    )

    def _compute_is_bundle(self):
        for module in self:
            module_info = self.get_module_info(module.name)
            module.is_bundle = module_info.get("bundle", False)

    def _get_modules_to_uninstall_for_bundle(self):
        self.ensure_one()
        downstream_dependencies = self.downstream_dependencies(self)
        other_installed_bundle_modules = self.search(
            [("state", "=", "installed"), ("id", "not in", downstream_dependencies.ids)]
        ).filtered(lambda m: m.is_bundle)
        modules_to_keep = self.search([("name", "in", conf.server_wide_modules)])
        modules_to_keep += other_installed_bundle_modules.upstream_dependencies(
            exclude_states=("uninstalled",)
        )
        modules_to_keep = set(modules_to_keep)
        modules_to_remove = self.upstream_dependencies(exclude_states=("uninstalled",))
        modules_to_remove = modules_to_remove.filtered(
            lambda d: d not in modules_to_keep
        )
        modules_to_remove += downstream_dependencies.upstream_dependencies(
            exclude_states=("uninstalled",)
        ).filtered(lambda d: d not in modules_to_keep and not d.is_bundle)
        modules_to_remove += modules_to_remove.downstream_dependencies(
            modules_to_remove
        ).filtered(lambda m: m not in downstream_dependencies)
        return modules_to_remove

    def button_uninstall(self):
        """
        Uninstall upstream modules but only if they're not in another bundle modules dependency.
        This will not be invoked if a dependency of a bundle is uninstalled, only when a bundle is directly uninstalled
        """
        modules = self.search(
            [("state", "=", "installed"), ("auto_install", "=", False)]
        )
        bundle_modules = modules.filtered(lambda m: m.is_bundle)
        for to_uninstall in self.filtered(lambda m: m in bundle_modules):
            modules_to_remove = to_uninstall._get_modules_to_uninstall_for_bundle()
            modules_to_remove.write({"state": "to remove"})

        return super().button_uninstall()

    @api.model_create_multi
    def create(self, vals_list):
        modules = super().create(vals_list)
        bundle_modules = self
        for module in modules:
            if module.get_module_info(module.name).get("bundle", False):
                bundle_modules += module
        bundle_modules.write({"module_type": "bundles"})
        return modules

    def _update_from_terp(self, terp):
        res = super()._update_from_terp(terp)
        self._update_module_type(terp)
        return res

    def _update_module_type(self, terp):
        if terp.get("bundle", False):
            self.module_type = "bundles"
        elif self.module_type == "bundles":
            self.module_type = "official"
