from odoo import api, fields, models


class RetiredModuleWizard(models.TransientModel):
    _name = "retired.module.wizard"
    _description = "Retired Modules"

    retired_module_ids = fields.Many2many(
        comodel_name="ir.module.module",
        string="Retired Modules",
        domain=[("state", "=", "installed")],
        default=lambda self: self._default_retired_module_ids(),
    )

    def _default_retired_module_ids(self):
        return self._get_retired_modules()

    @api.model
    def _get_exempt_modules(self):
        special_modules = ["container_s3"]  # TODO: Make this configurable
        modules = self.env["ir.module.module"].search([("state", "=", "installed")])
        exempt_modules = modules.filtered(
            lambda m: m.name in special_modules or m.name.startswith("theme_")
        )

        # Exempt payment providers from retirement if the payment module is installed
        payment_module = self.env.ref("base.module_payment")
        if payment_module.state == "installed":
            exempt_modules += (
                self.env["payment.provider"].search([]).mapped("module_id")
            )

        return exempt_modules

    @api.model
    def _get_retired_modules(self):
        modules = self.env["ir.module.module"].search([("state", "=", "installed")])
        bundles = modules.filtered(lambda m: m.is_bundle)

        current_modules = modules.filtered(lambda m: not m.auto_install)
        target_modules = bundles + bundles.upstream_dependencies(
            exclude_states=("uninstallable",)
        )
        exempt_modules = self._get_exempt_modules()
        target_modules += exempt_modules
        retired_modules = current_modules - target_modules
        return retired_modules

    def uninstall_retired_modules(self):
        retired_modules = self.retired_module_ids
        if retired_modules:
            retired_modules.button_immediate_uninstall()
