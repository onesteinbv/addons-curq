from odoo import SUPERUSER_ID, _, api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    vat_check_vies = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        rgs = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False)
        for company in companies:
            if not company.chart_template_id and rgs:
                rgs.with_user(SUPERUSER_ID)._load(company)

        return companies

    def get_unaffected_earnings_account(self):
        rgs = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False)
        if rgs:
            self = self.with_user(SUPERUSER_ID)
        return super(Company, self).get_unaffected_earnings_account()

    def _create_direct_debit_in_payment_mode(self):
        self.ensure_one()
        self = self.sudo()
        payment_mode = self.env["account.payment.mode"].search(
            [
                ("name", "=", "Direct debit"),
                ("company_id", "=", self.id),
            ],
            limit=1,
        )
        if payment_mode:
            return
        payment_method = self.env["account.payment.method"].search(
            [
                ("code", "=", "sepa_direct_debit"),
            ],
            limit=1,
        )
        bank_journal = self.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("company_id", "=", self.id),
            ],
            limit=1,
        )
        refund_payment_mode = self.env["account.payment.mode"].search(
            [
                ("name", "=", "Manual"),
                ("company_id", "=", self.id),
            ],
            limit=1,
        )
        if payment_method:
            self.env["account.payment.mode"].create(
                {
                    "name": "Direct debit",
                    "company_id": self.id,
                    "payment_method_id": payment_method.id,
                    "variable_journal_ids": bank_journal,
                    "bank_account_link": "variable",
                    "refund_payment_mode_id": refund_payment_mode.id,
                }
            )

    def _create_spread_templates(self):
        self.ensure_one()
        self = self.sudo()
        spread_journal = self.env["account.journal"].search(
            [
                ("code", "=", "ACCR"),
                ("company_id", "=", self.id),
            ],
            limit=1,
        )
        if not spread_journal:
            return
        spread_template = self.env["account.spread.template"].search(
            [
                ("company_id", "=", self.id),
            ],
            limit=1,
        )
        if spread_template:
            return
        accounts = self.env["account.account"].search(
            [
                ("company_id", "=", self.id),
                ("code", "in", ["4201080", "4206080", "4201160", "8002010", "8001010"]),
            ]
        )
        vals_list = [
            {
                "name": _("Onderhoud Gebouwen 12 maanden spreiding"),
                "company_id": self.id,
                "period_number": 12,
                "period_type": "month",
                "spread_type": "purchase",
                "spread_journal_id": spread_journal.id,
                "use_invoice_line_account": True,
                "exp_rev_account_id": accounts.filtered(
                    lambda a: a.code == "4201080"
                ).id,
            },
            {
                "name": _("Vakliteratuur 3 maanden spreiding"),
                "company_id": self.id,
                "period_number": 3,
                "period_type": "month",
                "spread_type": "purchase",
                "spread_journal_id": spread_journal.id,
                "use_invoice_line_account": True,
                "exp_rev_account_id": accounts.filtered(
                    lambda a: a.code == "4206080"
                ).id,
            },
            {
                "name": _("Assurantie Onroerende zaak 3 maanden spreiding"),
                "company_id": self.id,
                "period_number": 3,
                "period_type": "month",
                "spread_type": "purchase",
                "spread_journal_id": spread_journal.id,
                "use_invoice_line_account": True,
                "exp_rev_account_id": accounts.filtered(
                    lambda a: a.code == "4201160"
                ).id,
            },
            {
                "name": _("Omzet handelsgoederen 3 maanden spreiding"),
                "company_id": self.id,
                "period_number": 3,
                "period_type": "month",
                "spread_type": "sale",
                "spread_journal_id": spread_journal.id,
                "use_invoice_line_account": True,
                "exp_rev_account_id": accounts.filtered(
                    lambda a: a.code == "8002010"
                ).id,
            },
            {
                "name": _("Omzet productiegoederen 6 maanden spreiding"),
                "company_id": self.id,
                "period_number": 6,
                "period_type": "month",
                "spread_type": "sale",
                "spread_journal_id": spread_journal.id,
                "use_invoice_line_account": True,
                "exp_rev_account_id": accounts.filtered(
                    lambda a: a.code == "8001010"
                ).id,
            },
        ]
        self.env["account.spread.template"].create(vals_list)
