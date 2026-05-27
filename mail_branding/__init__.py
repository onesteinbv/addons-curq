from . import models
import base64
from odoo.tools.misc import file_path


def update_system_user(env):
    curq_icon_base64 = base64.b64encode(
        open(file_path("mail_branding/static/img/curqbot.png"), "rb").read()
    ).decode("utf-8")
    root_user_id = env.ref("base.user_root", raise_if_not_found=False)
    if root_user_id:
        root_user_id.with_context(mail_notrack=True).write(
            {"name": "CurqBot", "image_1920": curq_icon_base64}
        )


def uninstall_hook(env):
    """Uninstall hook for mail_branding module
    1. Change name of root user to OdooBot
    2. Change image of root user to Odoo icon
    3. Reset company colors to Odoo defaults
    """
    odoo_icon_base64 = base64.b64encode(
        open(file_path("mail/static/src/img/odoobot.png"), "rb").read()
    ).decode("utf-8")
    root_user_id = env.ref("base.user_root", raise_if_not_found=False)
    if root_user_id:
        root_user_id.with_context(mail_notrack=True).write(
            {"name": "OdooBot", "image_1920": odoo_icon_base64}
        )
    # Find the main company record (base.main_company)
    main_company = env.ref("base.main_company", raise_if_not_found=False)

    if main_company:
        # Writing False or None removes the custom hex codes,
        # forcing Odoo to fall back to its default system styling.
        main_company.write(
            {
                "primary_color": "#000000",
                "email_primary_color": "#000000",
                "secondary_color": "#875A7B",
                "email_secondary_color": "#875A7B",
            }
        )
