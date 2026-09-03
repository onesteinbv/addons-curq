from odoo import models


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    def _get_subscribers(self):
        """Remove unrestricted users from being added as followers for
        restricted user timesheet sheets"""
        subscribers = super()._get_subscribers()
        if self.user_id and self.user_id.is_restricted_user():
            subscribers -= self.env["res.partner"]._get_hidden_partners()
        return subscribers
