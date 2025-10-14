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
        count=False,
        access_rights_uid=None,
    ):
        # Purely for UX purposes
        model = self.with_user(access_rights_uid) if access_rights_uid else self
        if model.env.user.is_restricted_user():
            hidden_partners = (
                self.env["res.users"]
                .sudo()
                .with_context(active_test=False)
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
            count=count,
            access_rights_uid=access_rights_uid,
        )
