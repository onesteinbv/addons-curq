from odoo import api, models
from odoo.exceptions import AccessError


class BaseAutomation(models.Model):
    _inherit = "base.automation"

    @api.model
    def _get_groups_to_restrict_trigger_choices(self):
        """Hook to add groups to restrict choices.
        :type : list
        """
        return ["container_accessibility.group_restricted"]

    @api.model
    def _get_trigger_choices_to_restrict(self):
        """Hook to add choices to restrict.
        :type : list
        """
        # We only need the keys (the first element of the tuples) to filter effectively
        return ["on_create_or_write", "on_unlink", "on_change", "on_webhook"]

    @api.constrains("trigger")
    def _check_trigger_choice_selection(self):
        for record in self:
            if (
                any(
                    self.env.user.has_group(xml_id)
                    for xml_id in self._get_groups_to_restrict_trigger_choices()
                )
                and record.trigger in self._get_trigger_choices_to_restrict()
            ):
                human_readable_selection_string = self._fields[
                    "trigger"
                ].convert_to_export(record.trigger, self)
                raise AccessError(
                    self.env._(
                        f"Sorry, You are restricted to use '{human_readable_selection_string}' Trigger ! \n Please contact your system administrator."
                    )
                )

    @api.model
    def _get_trigger_selection_choices(self):
        """Returns the filtered selection list."""
        trigger_choices = self._fields["trigger"]._description_selection(self.env)
        if any(
            self.env.user.has_group(xml_id)
            for xml_id in self._get_groups_to_restrict_trigger_choices()
        ):
            to_restrict = self._get_trigger_choices_to_restrict()
            # Filter the list by checking if the key (item[0]) is in our removal set
            return [
                choice for choice in trigger_choices if choice[0] not in to_restrict
            ]

        return trigger_choices

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Filter selection options based on user group."""
        res = super().fields_get(allfields, attributes)
        # Check if 'trigger' is in the returned fields
        if "trigger" in res:
            res["trigger"]["selection"] = self._get_trigger_selection_choices()
        return res

    def _update_cron(self):
        sudo_self = self
        if self.env.user.is_restricted_user() and self.env.user.has_group(
            "base.group_system"
        ):
            sudo_self = self.sudo()
        return super(BaseAutomation, sudo_self)._update_cron()
