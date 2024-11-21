# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    auditlog_rule_model = env["auditlog.rule"]
    account_analytic_line_model_id = env.ref(
        "hr_timesheet.model_account_analytic_line"
    ).id
    timesheet_auditlog_rule = auditlog_rule_model.search(
        [("model_id", "=", account_analytic_line_model_id)], limit=1
    )
    if timesheet_auditlog_rule:
        if not timesheet_auditlog_rule.log_unlink:
            if timesheet_auditlog_rule.state != "draft":
                timesheet_auditlog_rule.state = "draft"
                timesheet_auditlog_rule.write(
                    {"state": "subscribed", "log_unlink": True}
                )
            else:
                timesheet_auditlog_rule.log_unlink = True
    else:
        auditlog_rule_model.create(
            {
                "name": "Timesheet",
                "model_id": account_analytic_line_model_id,
                "log_type": "fast",
                "log_unlink": True,
                "log_create": False,
                "log_write": False,
                "log_export_data": False,
                "state": "subscribed",
            }
        )
