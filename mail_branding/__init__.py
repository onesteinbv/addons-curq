from . import models
import base64
from odoo.tools.misc import file_path


def uninstall_hook(env):
    """Uninstall hook for mail_branding module
    1. Change name of root user to OdooBot
    2. Change image of root user to Odoo icon
    3. Reset overridden fields in ir.model.fields and selection
    """
    odoo_icon_base64 = base64.b64encode(
        open(file_path("mail/static/src/img/odoobot.png"), "rb").read()
    ).decode("utf-8")
    root_user_id = env.ref("base.user_root", raise_if_not_found=False)
    if root_user_id:
        root_user_id.with_context(mail_notrack=True).write(
            {"name": "OdooBot", "image_1920": odoo_icon_base64}
        )

    # Revert overridden fields in ir.model.fields
    odoobot_field = env["ir.model.fields"].search(
        [
            ("model", "=", "res.users"),
            ("name", "=", "odoobot_state"),
        ]
    )
    if odoobot_field:
        odoobot_field.write({"field_description": "OdooBot Status"})

    notification_field = env["ir.model.fields"].search(
        [
            ("model", "=", "res.users"),
            ("name", "=", "notification_type"),
        ]
    )
    if notification_field:
        notification_field.write(
            {
                "help": "Policy on how to handle Chatter notifications:\n"
                "- Handle by Emails: notifications are sent to your email address\n"
                "- Handle in Odoo: notifications appear in your Odoo Inbox"
            }
        )

    inbox_selection = env["ir.model.fields.selection"].search(
        [
            ("field_id.model", "=", "res.users"),
            ("field_id.name", "=", "notification_type"),
            ("value", "=", "inbox"),
        ]
    )
    if inbox_selection:
        inbox_selection.write({"name": "Handle in Odoo"})
