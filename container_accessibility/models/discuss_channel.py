from odoo import models


class Channel(models.Model):
    _inherit = "discuss.channel"

    def _subscribe_users_automatically_get_members(self):
        res = super(Channel, self.sudo())._subscribe_users_automatically_get_members()
        # Exclude hidden partners from the list
        hidden_partners = self.env["res.partner"]._get_hidden_partners()
        for channel in res:
            res[channel] = list(set(res[channel]) - set(hidden_partners.ids))
        return res

    def _subscribe_users_automatically(self):
        res = super(Channel, self)._subscribe_users_automatically()
        # Make sure there are never hidden (non-restrictive) partners in channels
        hidden_partners = self.env["res.partner"]._get_hidden_partners()
        self.env["discuss.channel.member"].sudo().search(
            [("channel_id", "in", self.ids), ("partner_id", "in", hidden_partners.ids)]
        ).unlink()
        return res
