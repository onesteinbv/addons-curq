from odoo import api, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        chart_template = self.env.company.chart_template
        is_rgs = chart_template == "nl_rgs"
        if is_rgs:
            # Bank
            is_bank = self.env.context.get("domain_account_journal_type") == "bank"
            if is_bank:
                bank_prefix = self.env.company.bank_account_code_prefix
                if bank_prefix and operator == "ilike":
                    args = args or []
                    args = [("code", "=ilike", bank_prefix + "%")] + args
            # Cash
            is_cash = self.env.context.get("domain_account_journal_type") == "cash"
            if is_cash:
                cash_prefix = self.env.company.cash_account_code_prefix
                if cash_prefix and operator == "ilike":
                    args = args or []
                    args = [("code", "=ilike", cash_prefix + "%")] + args
        return super().name_search(name, args=args, operator=operator, limit=limit)
