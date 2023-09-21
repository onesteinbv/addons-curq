# Copyright 2023 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Online Bank Statements: MyPonto.com - LOG",
    "version": "16.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/OCA/bank-statement-import",
    "author": "Onestein",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account_statement_import_online_ponto"],
    "data": [
        "security/ir.model.access.csv",
        "views/ponto_log.xml",
    ],
}
