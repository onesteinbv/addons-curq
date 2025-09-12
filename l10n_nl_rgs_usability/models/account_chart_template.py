import re

from odoo import api, models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _load(self, company):
        res = super(AccountChartTemplate, self)._load(company)

        # Generate payment modes
        self._generate_payment_modes(company)
        # Generate spread templates
        company._create_spread_templates()
        return res

    @api.model
    def _generate_payment_modes(self, company):
        """Generate payment modes"""
        bank_journal = self.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("company_id", "=", company.id),
            ],
            limit=1,
        )
        if not bank_journal:
            return
        payment_mode_vals = [
            {
                "name": "Manual",
                "company_id": company.id,
                "bank_account_link": "variable",
                "payment_method_id": self.env.ref(
                    "account.account_payment_method_manual_out"
                ).id,
                "sequence": 10,
            },
            {
                "name": "Ideal",
                "company_id": company.id,
                "bank_account_link": "variable",
                "payment_method_id": self.env.ref(
                    "account.account_payment_method_manual_out"
                ).id,
                "sequence": 11,
            },
            {
                "name": "Incasso",
                "company_id": company.id,
                "bank_account_link": "variable",
                "payment_method_id": self.env.ref(
                    "account.account_payment_method_manual_out"
                ).id,
                "sequence": 12,
            },
            {
                "name": "Credit Card",
                "company_id": company.id,
                "bank_account_link": "variable",
                "payment_method_id": self.env.ref(
                    "account.account_payment_method_manual_out"
                ).id,
                "sequence": 13,
            },
            {
                "name": "European payments (SEPA)",
                "company_id": company.id,
                "bank_account_link": "fixed",
                "payment_method_id": self.env.ref(
                    "account_banking_sepa_credit_transfer.sepa_credit_transfer"
                ).id,
                "payment_order_ok": True,
                "default_date_prefered": "due",
                "fixed_journal_id": bank_journal.id,
                "sequence": 14,
            },
        ]
        module = "l10n_nl_rgs_usability"
        data_list = []
        for vals in payment_mode_vals:
            xml_id = "%s.%s_%s" % (
                module,
                company.id,
                re.sub("[^a-zA-Z]+", "", vals["name"].lower()),
            )
            data_list.append(dict(xml_id=xml_id, values=vals, noupdate=True))
        res = self.env["account.payment.mode"]._load_records(data_list)
        company._create_direct_debit_in_payment_mode()
        return res
