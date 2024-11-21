from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            "free_member",
            "membership_category_ids",
            "is_adhered_member",
            "membership_state",
            "associate_member",
            "membership_start",
            "membership_start_adhered",
            "membership_last_start",
            "membership_stop",
            "membership_cancel",
            "member_lines",
            "membership_group_member_ids",
            "subscription_ids",
        ]
