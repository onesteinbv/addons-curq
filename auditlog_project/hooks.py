# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    auditlog_rule_model = env["auditlog.rule"]
    project_model_id = env.ref("project.model_project_project").id
    project_task_model_id = env.ref("project.model_project_task").id
    project_auditlog_rule = auditlog_rule_model.search(
        [("model_id", "=", project_model_id)], limit=1
    )
    if project_auditlog_rule:
        if not project_auditlog_rule.log_unlink:
            if project_auditlog_rule.state != "draft":
                project_auditlog_rule.state = "draft"
                project_auditlog_rule.write({"state": "subscribed", "log_unlink": True})
            else:
                project_auditlog_rule.log_unlink = True
    else:
        auditlog_rule_model.create(
            {
                "name": "Project",
                "model_id": project_model_id,
                "log_type": "fast",
                "log_unlink": True,
                "log_create": False,
                "log_write": False,
                "log_export_data": False,
                "state": "subscribed",
            }
        )
    project_task_auditlog_rule = auditlog_rule_model.search(
        [("model_id", "=", project_task_model_id)], limit=1
    )
    if project_task_auditlog_rule:
        if not project_task_auditlog_rule.log_unlink:
            if project_task_auditlog_rule.state != "draft":
                project_task_auditlog_rule.state = "draft"
                project_task_auditlog_rule.write(
                    {"state": "subscribed", "log_unlink": True}
                )
            else:
                project_task_auditlog_rule.log_unlink = True
    else:
        auditlog_rule_model.create(
            {
                "name": "Project Task",
                "model_id": project_task_model_id,
                "log_type": "fast",
                "log_unlink": True,
                "log_create": False,
                "log_write": False,
                "log_export_data": False,
                "state": "subscribed",
            }
        )
