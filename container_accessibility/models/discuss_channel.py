from odoo import models


class Channel(models.Model):
    _inherit = "discuss.channel"

    def _subscribe_users_automatically_get_members(self):
        # Default channels have auto-subscription including non-restricted users
        return super(Channel, self.sudo())._subscribe_users_automatically_get_members()
