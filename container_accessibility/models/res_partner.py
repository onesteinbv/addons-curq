from odoo import api, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(
        self,
        domain,
        offset=0,
        limit=None,
        order=None,
    ):
        # Purely for UX purposes
        if self.env.user.is_restricted_user() and not self.env.su:
            hidden_partners = self._get_hidden_partners()
            domain = expression.AND([domain, [("id", "not in", hidden_partners.ids)]])
        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
        )

    @api.model
    def _get_hidden_partners(self):
        """Returns the hidden partners for restricted users."""
        hidden_roles = [
            self.env.ref("container_accessibility.role_administrator").id,
            False,
        ]

        hidden_partners = (
            self.env["res.users"]
            .sudo()
            .with_context(active_test=False)
            .search([("role_id", "not in", hidden_roles)])
            .mapped("partner_id")
        )
        return hidden_partners
