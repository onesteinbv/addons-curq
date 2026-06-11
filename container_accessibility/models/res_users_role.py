from odoo import fields, models
from odoo.osv import expression


class ResUsersRole(models.Model):
    _inherit = "res.users.role"

    implied_by_text = fields.Text(
        string="Implied by",
        inverse="_inverse_implied_by_text",
        help="Textual representation of the groups of this role. Seperated by new lines.",
    )

    def apply_implied_by_text(self, ignore=None):
        for role in self:
            xml_ids = role.implied_by_text.strip().split("\n")
            if ignore:
                xml_ids = [xml_id for xml_id in xml_ids if xml_id not in ignore]

            # Search directly the groups through their xml ids instead of using env.ref that is cached
            xml_ids = [xml_id.split(".") for xml_id in xml_ids]
            domain = expression.OR(
                [
                    [("module", "=", xml_id[0]), ("name", "=", xml_id[1])]
                    for xml_id in xml_ids
                ]
            )
            domain = expression.AND([[("model", "=", "res.groups")], domain])
            model_datas = self.env["ir.model.data"].search(domain)
            assert all(model_data.model == "res.groups" for model_data in model_datas)
            groups = model_datas.mapped("res_id")
            role.implied_ids = groups

    def _inverse_implied_by_text(self):
        self.apply_implied_by_text()
