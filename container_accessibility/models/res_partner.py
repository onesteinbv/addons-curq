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
        # Purely for UX purposes, removes all partners related to users outside of the
        # container_accessibility.role_manager, container_accessibility.role_user, and
        # container_accessibility.role_accountant roles
        # from the search results.
        if (
            not self.env.su
            and self.env.user.role_id
            and self.env.user.role_id
            != self.env.ref("container_accessibility.role_administrator")
        ):
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
        role_administrator = self.env.ref("container_accessibility.role_administrator")
        hidden_roles = [role_administrator.id, False]

        hidden_partners = (
            self.env["res.users"]
            .sudo()
            .with_context(active_test=False)
            .search([("role_id", "in", hidden_roles)])
            .mapped("partner_id")
        )
        return hidden_partners
