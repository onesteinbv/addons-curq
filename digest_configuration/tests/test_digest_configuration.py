from odoo.tests import common

from ..hooks import post_init_hook


class TestDigestConfiguration(common.SingleTransactionCase):
    def test_post_init_hook(self):
        ir_config_parameter_obj = self.env["ir.config_parameter"]
        ir_config_parameter_obj.create(
            {"key": "digest.default_digest_emails", "value": "True"}
        )
        post_init_hook(self.env)
        self.assertFalse(
            ir_config_parameter_obj.search(
                [("key", "=", "digest.default_digest_emails")]
            )
        )
