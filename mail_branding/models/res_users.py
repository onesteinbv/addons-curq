from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    notification_type = fields.Selection(
        selection_add=[("inbox", "Handle in CURQ")],
        help="Policy on how to handle Chatter notifications:\n"
        "- By Emails: notifications are sent to your email address\n"
        "- In CURQ: notifications appear in your CURQ Inbox",
    )

    odoobot_state = fields.Selection(string="CURQBot Status")
