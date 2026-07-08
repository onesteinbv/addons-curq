from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def button_install(self):
        self_sudo = self

        # Make an exception for the administrator role, so that restricted users with this role can install bundles.
        if (
            self.env.user.is_restricted_user()
            and self.env.user.role_id
            == self.env.ref("container_accessibility.role_administrator")
            and not self.env.su
        ):
            filtered = self._filtered_access("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_install()

    def button_upgrade(self):
        self_sudo = self

        # Make an exception for the administrator role, so that restricted users with this role can upgrade bundles.
        if (
            self.env.user.is_restricted_user()
            and self.env.user.role_id
            == self.env.ref("container_accessibility.role_administrator")
            and not self.env.su
        ):
            filtered = self._filtered_access("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_upgrade()

    def button_uninstall(self):
        self_sudo = self

        # Make an exception for the administrator role, so that restricted users with this role can uninstall bundles.
        if (
            self.env.user.is_restricted_user()
            and self.env.user.role_id
            == self.env.ref("container_accessibility.role_administrator")
            and not self.env.su
        ):
            filtered = self._filtered_access("write")
            if filtered:
                self_sudo = self.sudo()
        return super(IrModuleModule, self_sudo).button_uninstall()
