from odoo import api, models
from odoo.exceptions import AccessError


class IrActionsServer(models.Model):
    _inherit = "ir.actions.server"

    @api.model
    def _get_groups_to_restrict_state_choices(self):
        """Hook to add groups to remove choices.
        :type : list
        """
        return ["container_accessibility.group_restricted"]

    @api.model
    def _get_state_choices_to_restrict(self):
        """Hook to add choices to remove.
        :type : list
        """
        # We only need the keys (the first element of the tuples) to filter effectively
        return ["code"]

    @api.constrains("state")
    def _check_trigger_state_selection(self):
        for record in self:
            if (
                any(
                    self.env.user.has_group(xml_id)
                    for xml_id in self._get_groups_to_restrict_state_choices()
                )
                and record.state in self._get_state_choices_to_restrict()
            ):
                human_readable_selection_string = self._fields[
                    "state"
                ].convert_to_export(record.state, self)
                raise AccessError(
                    self.env._(
                        f"Sorry, You are restricted to use '{human_readable_selection_string}' Type of Server Action! Please contact your system administrator."
                    )
                )

    @api.model
    def _get_state_selection_choices(self):
        """Returns the filtered selection list based on user groups."""
        choices = self._fields["state"]._description_selection(self.env)
        if any(
            self.env.user.has_group(group_xml_id)
            for group_xml_id in self._get_groups_to_restrict_state_choices()
        ):
            to_restrict = self._get_state_choices_to_restrict()
            return [c for c in choices if c[0] not in to_restrict]

        return choices

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Filter selection options based on user group."""
        res = super().fields_get(allfields, attributes)
        # Check if 'state' is in the returned fields
        if "state" in res:
            res["state"]["selection"] = self._get_state_selection_choices()
        return res
