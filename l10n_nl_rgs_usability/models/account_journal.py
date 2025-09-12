from odoo import _, api, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.depends("type", "currency_id")
    def _compute_outbound_payment_method_line_ids(self):
        res = super()._compute_outbound_payment_method_line_ids()
        self._set_journal_bank_payment_credit_account()
        return res

    def _set_journal_bank_payment_credit_account(self):
        for journal in self.filtered(lambda j: j.type == "bank"):
            if journal.company_id.chart_template_id == self.env.ref(
                "l10n_nl_rgs.l10nnl_rgs_chart_template", False
            ):
                lines = journal.outbound_payment_method_line_ids
                sepa_lines = lines.filtered(
                    lambda l: l.payment_method_id.code == "sepa_credit_transfer"
                )
                for line in sepa_lines:
                    if not line.payment_account_id:
                        line.payment_account_id = (
                            journal.company_id.account_journal_payment_credit_account_id
                        )

    def unlink(self):
        if self.env.context.get("force_delete"):
            for journal in self:
                payment_modes = self.env["account.payment.mode"].search(
                    [
                        ("fixed_journal_id", "=", journal.id),
                    ]
                )
                payment_modes.unlink()
        return super().unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "check_chronology" not in vals and vals.get("type") == "purchase":
                vals["check_chronology"] = True
        return super().create(vals_list)

    @api.onchange("type")
    def _onchange_type(self):
        res = super()._onchange_type()
        if self.type in ["sale"]:
            self.check_chronology = True
        else:
            self.check_chronology = False
        if isinstance(self.id, models.NewId) and self.type == "bank":
            self.type = False
            warning = {
                "title": _("Warning for bank journal"),
                "message": _(
                    "Please add your bank number in menu 'Add a Bank Account'."
                ),
            }
            return {"warning": warning}
        return res
