from odoo import api, models
from odoo.osv import expression


class ModelData(models.Model):
    _inherit = "ir.model.data"

    def create(self, vals):
        res = super().create(vals)
        if vals.get("model") == "res.groups":
            self.env["res.users.role"].search(
                [("implied_by_text", "ilike", res.complete_name)]
            ).apply_implied_by_text()
        return res

    def write(self, values):
        xml_ids = self.mapped("complete_name")
        res = super().write(values)
        xml_ids += self.mapped("complete_name")
        if "res.groups" in self.mapped("model"):
            domain = expression.OR(
                [[("implied_by_text", "ilike", xml_id)] for xml_id in xml_ids]
            )
            affected_roles = self.env["res.users.role"].search(domain)
            affected_roles.apply_implied_by_text()
        return res

    @api.ondelete(at_uninstall=False)
    def _unlink_affected_roles(self):
        xml_ids = self.filtered(lambda d: d.model == "res.groups").mapped(
            "complete_name"
        )
        if not xml_ids:
            return
        domain = expression.OR(
            [[("implied_by_text", "ilike", xml_id)] for xml_id in xml_ids]
        )
        affected_roles = self.env["res.users.role"].search(domain)
        affected_roles.apply_implied_by_text(ignore=xml_ids)
