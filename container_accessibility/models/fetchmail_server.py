from odoo import api, fields, models


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    private = fields.Boolean(string="Is private server")

    @api.model
    def _update_cron(self):
        sudo_self = self
        if self.env.user.is_restricted_user() and self.env.user.has_group(
            "base.group_system"
        ):
            sudo_self = self.sudo()
        return super(FetchmailServer, sudo_self)._update_cron()
