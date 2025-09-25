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
            hidden_partners = (
                self.env["res.users"]
                .sudo()
                .search(
                    [
                        (
                            "groups_id",
                            "not in",
                            [
                                self.env.ref("base.group_portal").id,
                                self.env.ref(
                                    "container_accessibility.group_restricted"
                                ).id,
                            ],
                        )
                    ]
                )
                .mapped("partner_id")
            )
            domain = expression.AND([domain, [("id", "not in", hidden_partners.ids)]])
        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
        )
