from odoo.tests.common import TransactionCase


class TestViewBranding(TransactionCase):
    def test_view_branding(self):
        res = self.env["res.config.settings"].get_views([[False, "form"]])
        self.assertNotIn("Odoo", res["views"]["form"]["arch"])
