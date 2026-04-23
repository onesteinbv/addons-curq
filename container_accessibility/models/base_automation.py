from odoo import api, fields, models

TRIGGER_CHOICES = [
    ("on_stage_set", "Stage is set to"),
    ("on_user_set", "User is set"),
    ("on_tag_set", "Tag is added"),
    ("on_state_set", "State is set to"),
    ("on_priority_set", "Priority is set to"),
    ("on_archive", "On archived"),
    ("on_unarchive", "On unarchived"),
    ("on_create_or_write", "On save"),
    ("on_create", "On creation"),  # deprecated, use 'on_create_or_write' instead
    ("on_write", "On update"),  # deprecated, use 'on_create_or_write' instead
    ("on_unlink", "On deletion"),
    ("on_change", "On UI change"),
    ("on_time", "Based on date field"),
    ("on_time_created", "After creation"),
    ("on_time_updated", "After last update"),
    ("on_message_received", "On incoming message"),
    ("on_message_sent", "On outgoing message"),
    ("on_webhook", "On webhook"),
]


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

    @api.model
    def _get_trigger_selection_choices(self):
        """Returns the filtered selection list."""
        if any(
            self.env.user.has_group(xml_id)
            for xml_id in self._get_groups_to_restrict_trigger_choices()
        ):
            to_restrict = self._get_trigger_choices_to_restrict()
            # Filter the list by checking if the key (item[0]) is in our removal set
            return [
                choice for choice in TRIGGER_CHOICES if choice[0] not in to_restrict
            ]

        return TRIGGER_CHOICES

    trigger = fields.Selection(
        selection=lambda self: self._get_trigger_selection_choices()
    )

    def _update_cron(self):
        sudo_self = self
        if self.env.user.is_restricted_user() and self.env.user.has_group(
            "base.group_system"
        ):
            sudo_self = self.sudo()
        return super(BaseAutomation, sudo_self)._update_cron()
