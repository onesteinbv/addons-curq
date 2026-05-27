from odoo import fields, models


class ResUsersPreferences(models.Model):
    _inherit = "res.users"

    notification_type = fields.Selection(
        selection_add=[("inbox", "In Curq")],
        help="Policy on how to handle Chatter notifications:\n"
        "- By Emails: notifications are sent to your email address\n"
        "- In Curq: notifications appear in your Curq Inbox",
    )

    odoobot_state = fields.Selection(string="CurqBot Status")
