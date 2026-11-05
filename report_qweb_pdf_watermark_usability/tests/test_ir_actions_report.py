import base64

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestReportWatermark(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report = cls.env["ir.actions.report"]
        cls.sample_report = cls.report.create(
            {
                "name": "Test Sample Report",
                "model": "res.partner",
                "report_type": "qweb-pdf",
                "report_name": "test.sample_report",
                "use_company_watermark": False,
            }
        )
        cls.env["ir.model.data"].create(
            {
                "name": "test_sample_report",
                "module": "report_qweb_pdf_watermark_usability",
                "model": "ir.actions.report",
                "res_id": cls.sample_report.id,
            }
        )

    def test_add_watermark_reports(self):
        """Pass a list of report IDs to add_watermark_reports."""
        self.assertFalse(self.sample_report.use_company_watermark)
        self.env["res.config.settings"].add_watermark_reports([self.sample_report.id])
        self.assertTrue(self.sample_report.use_company_watermark)

    def test_add_watermark_reports_with_invalid_types_raises_error(self):
        """Passing non-list types (int, recordset, False, None) raises TypeError."""
        for invalid_val in (
            self.sample_report.id,
            self.sample_report,
            False,
            None,
            "1,2",
        ):
            with self.subTest(invalid_val=invalid_val):
                with self.assertRaises(TypeError):
                    self.env["res.config.settings"].add_watermark_reports(invalid_val)

    def test_add_watermark_reports_empty_list(self):
        """Pass empty list [] to add_watermark_reports without errors."""
        self.assertFalse(self.sample_report.use_company_watermark)
        self.env["res.config.settings"].add_watermark_reports([])
        self.assertFalse(self.sample_report.use_company_watermark)

    def test_add_watermark_reports_missing_ids_handled_gracefully(self):
        """Invalid, None, False, or nonexistent IDs must not raise exceptions,
        and valid report IDs in the same call must still be enabled.
        """
        self.assertFalse(self.sample_report.use_company_watermark)
        try:
            self.env["res.config.settings"].add_watermark_reports(
                [False, None, 999999, self.sample_report.id]
            )
        except Exception as e:
            self.fail(f"add_watermark_reports raised an unexpected exception: {e}")
        self.assertTrue(self.sample_report.use_company_watermark)

    def test_add_watermark_reports_ignores_non_pdf(self):
        """Non-PDF reports (e.g. qweb-text, qweb-html) must not be enabled."""
        text_report = self.report.create(
            {
                "name": "Test Text Report",
                "model": "res.partner",
                "report_type": "qweb-text",
                "report_name": "test.text_report",
                "use_company_watermark": False,
            }
        )
        self.env["res.config.settings"].add_watermark_reports([text_report.id])
        self.assertFalse(text_report.use_company_watermark)

    def test_add_watermark_reports_already_enabled(self):
        """Reports already having use_company_watermark=True remain enabled."""
        self.sample_report.use_company_watermark = True
        self.env["res.config.settings"].add_watermark_reports([self.sample_report.id])
        self.assertTrue(self.sample_report.use_company_watermark)

    def test_add_watermark_reports_preserves_custom_watermark(self):
        """Reports with binary pdf_watermark must not have company watermark enabled."""
        dummy_b64 = base64.b64encode(b"dummy_content").decode("utf-8")
        custom_watermark_report = self.report.create(
            {
                "name": "Test Custom Watermark Report",
                "model": "res.partner",
                "report_type": "qweb-pdf",
                "report_name": "test.custom_watermark_report",
                "use_company_watermark": False,
                "pdf_watermark": dummy_b64,
            }
        )
        self.env["res.config.settings"].add_watermark_reports(
            [custom_watermark_report.id]
        )
        self.assertFalse(custom_watermark_report.use_company_watermark)

        values = self.env["res.config.settings"].get_values()
        self.assertNotIn(
            custom_watermark_report.id,
            values["outgoing_report_config_ids"][0][2],
        )

    def test_add_watermark_reports_preserves_expression_watermark(self):
        """Reports with pdf_watermark_expression must
        not have company watermark enabled."""
        expr_watermark_report = self.report.create(
            {
                "name": "Test Expression Watermark Report",
                "model": "res.partner",
                "report_type": "qweb-pdf",
                "report_name": "test.expr_watermark_report",
                "use_company_watermark": False,
                "pdf_watermark_expression": "dummy_expression",
            }
        )
        self.env["res.config.settings"].add_watermark_reports(
            [expr_watermark_report.id]
        )
        self.assertFalse(expr_watermark_report.use_company_watermark)

        values = self.env["res.config.settings"].get_values()
        self.assertNotIn(
            expr_watermark_report.id,
            values["outgoing_report_config_ids"][0][2],
        )

    def test_set_and_get_values_with_config_param(self):
        """Test set_values and get_values flow with ir.config_parameter."""
        second_report = self.report.create(
            {
                "name": "Test Second Report",
                "model": "res.partner",
                "report_type": "qweb-pdf",
                "report_name": "test.second_report",
                "use_company_watermark": False,
            }
        )
        settings = self.env["res.config.settings"].create(
            {
                "outgoing_report_config_ids": [
                    (6, 0, [self.sample_report.id, second_report.id])
                ],
            }
        )
        settings.set_values()

        self.assertTrue(self.sample_report.use_company_watermark)
        self.assertTrue(second_report.use_company_watermark)

        values = self.env["res.config.settings"].get_values()
        configured_ids = values["outgoing_report_config_ids"][0][2]
        self.assertIn(self.sample_report.id, configured_ids)
        self.assertIn(second_report.id, configured_ids)

        # Now remove second_report and call set_values
        settings_update = self.env["res.config.settings"].create(
            {
                "outgoing_report_config_ids": [(6, 0, [self.sample_report.id])],
            }
        )
        settings_update.set_values()

        # Previous value compared: second_report should now be disabled
        self.assertTrue(self.sample_report.use_company_watermark)
        self.assertFalse(second_report.use_company_watermark)

        values_after = self.env["res.config.settings"].get_values()
        configured_ids_after = values_after["outgoing_report_config_ids"][0][2]
        self.assertIn(self.sample_report.id, configured_ids_after)
        self.assertNotIn(second_report.id, configured_ids_after)

    def test_create_with_link_command_merges_previous_and_new_ids(self):
        """When a child module installs via create() with (4, ID), it should
        preserve previous reports and append the new report to ir.config_parameter."""
        # 1. Start with sample_report already configured
        self.env["res.config.settings"].create(
            {
                "outgoing_report_config_ids": [(6, 0, [self.sample_report.id])],
            }
        ).set_values()
        self.assertTrue(self.sample_report.use_company_watermark)

        # 2. Child module installs and calls create() with (4, new_id)
        third_report = self.report.create(
            {
                "name": "Test Third Report",
                "model": "res.partner",
                "report_type": "qweb-pdf",
                "report_name": "test.third_report",
                "use_company_watermark": False,
            }
        )
        self.env["res.config.settings"].with_context(watermark_append_mode=True).create(
            {
                "outgoing_report_config_ids": [(4, third_report.id)],
            }
        )

        # Both previous (sample_report) and new (third_report) must be active and stored
        self.assertTrue(self.sample_report.use_company_watermark)
        self.assertTrue(third_report.use_company_watermark)

        values = self.env["res.config.settings"].get_values()
        configured_ids = values["outgoing_report_config_ids"][0][2]
        self.assertIn(self.sample_report.id, configured_ids)
        self.assertIn(third_report.id, configured_ids)
