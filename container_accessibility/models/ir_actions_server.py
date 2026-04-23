from odoo import api, fields, models

# Move constants into a mapping for cleaner iteration
MODULE_STATE_MAPPING = {
    "mail": [
        ("next_activity", "Create Activity"),
        ("mail_post", "Send Email"),
        ("followers", "Add Followers"),
        ("remove_followers", "Remove Followers"),
    ],
    "server_action_mass_edit": [("mass_edit", "Mass Edit Records")],
    "sms": [("sms", "Send SMS")],
}

STATE_CHOICES_BASE = [
    ("object_write", "Update Record"),
    ("object_create", "Create Record"),
    ("code", "Execute Code"),
    ("webhook", "Send Webhook Notification"),
    ("multi", "Execute Existing Actions"),
]


class IrActionsServer(models.Model):
    _inherit = "ir.actions.server"

    @api.model
    def _get_all_state_choices(self):
        """Combines base choices with installed module choices, ensuring uniqueness."""
        # Use a dict to automatically handle overrides/duplicates by key
        choices_dict = dict(STATE_CHOICES_BASE)

        # Filter for installed modules in one go
        installed_modules = (
            self.env["ir.module.module"]
            .sudo()
            .search(
                [
                    ("name", "in", list(MODULE_STATE_MAPPING.keys())),
                    ("state", "=", "installed"),
                ]
            )
            .mapped("name")
        )

        for module in installed_modules:
            choices_dict.update(dict(MODULE_STATE_MAPPING[module]))

        return list(choices_dict.items())

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

    @api.model
    def _get_state_selection_choices(self):
        """Returns the filtered selection list based on user groups."""
        choices = self._get_all_state_choices()
        if any(
            self.env.user.has_group(group_xml_id)
            for group_xml_id in self._get_groups_to_restrict_state_choices()
        ):
            to_restrict = self._get_state_choices_to_restrict()
            return [c for c in choices if c[0] not in to_restrict]

        return choices

    state = fields.Selection(selection=lambda self: self._get_state_selection_choices())
