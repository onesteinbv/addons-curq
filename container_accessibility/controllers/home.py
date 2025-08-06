from odoo import _, http
from odoo.exceptions import AccessError

from odoo.addons.web.controllers.home import Home


class HomeController(Home):
    @http.route()
    def switch_to_admin(self):
        raise AccessError(
            _("Access Denied")
        )  # Disable this function all together even for admins
