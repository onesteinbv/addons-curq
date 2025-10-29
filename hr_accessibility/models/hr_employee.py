from odoo import api, models
from odoo.osv import expression


class HrEmployee(models.Model):
    _inherit = "hr.employee"

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
            hidden_employees = (
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
                .mapped("employee_ids")
            )
            domain = expression.AND([domain, [("id", "not in", hidden_employees.ids)]])
        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
        )
