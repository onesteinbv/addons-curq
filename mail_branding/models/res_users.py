from odoo import api, models


class ResUsersPreferences(models.Model):
    _inherit = "res.users"

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """
        Modify the labels of:
            - odoobot_state: OdooBot Status to CurqBot Status
            - notification_type: Notification Selection label to Curq from Odoo.
        """
        res = super().fields_get(allfields, attributes)
        if "odoobot_state" in res:
            res["odoobot_state"]["string"] = "CurqBot Status"
        if "notification_type" in res:
            choices = self._fields["notification_type"]._description_selection(self.env)
            new_choices = []
            for choice in choices:
                new_choices.append((choice[0], choice[1].replace("Odoo", "Curq")))
            res["notification_type"]["selection"] = new_choices
        return res
