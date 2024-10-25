from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def button_immediate_install(self):
        self_sudo = self
        if self.env.user.is_restricted_user() and not self.env.su:
            filtered = self._filter_access_rules("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_immediate_install()

    def button_immediate_upgrade(self):
        self_sudo = self
        if self.env.user.is_restricted_user() and not self.env.su:
            filtered = self._filter_access_rules("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_immediate_upgrade()

    def button_immediate_uninstall(self):
        self_sudo = self
        if self.env.user.is_restricted_user() and not self.env.su:
            filtered = self._filter_access_rules("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_immediate_uninstall()
