from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def button_install(self):
        self_sudo = self
        if self.env.user.is_restricted_user() and not self.env.su:
            filtered = self._filtered_access("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_install()

    def button_upgrade(self):
        self_sudo = self
        if self.env.user.is_restricted_user() and not self.env.su:
            filtered = self._filtered_access("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_upgrade()

    def button_uninstall(self):
        self_sudo = self
        if self.env.user.is_restricted_user() and not self.env.su:
            filtered = self._filtered_access("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_uninstall()
