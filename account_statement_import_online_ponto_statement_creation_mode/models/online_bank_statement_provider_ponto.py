# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class OnlineBankStatementProvider(models.Model):
    _inherit = "online.bank.statement.provider"

    @api.onchange("service")
    def _onchange_service(self):
        if self.service == "ponto":
            self.statement_creation_mode = "monthly"
