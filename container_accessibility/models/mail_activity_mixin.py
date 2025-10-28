from odoo import models


class MailActivityMixin(models.AbstractModel):
    _inherit = "mail.activity.mixin"

    def activity_schedule(
        self, act_type_xmlid="", date_deadline=None, summary="", note="", **act_values
    ):
        sudo_self = self
        if self.env.user.is_restricted_user() and not self.env.su:
            sudo_self = self.sudo()
        return super(MailActivityMixin, sudo_self).activity_schedule(
            act_type_xmlid, date_deadline, summary, note, **act_values
        )
