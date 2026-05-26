from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _get_default_release_note_version(self):
        # New users should have the current version as their last read version
        # to avoid showing the release note wizard on their first login.

        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("release_note.current_version")
        )

    last_release_note_version = fields.Char(
        help="The last release note version that the user has read.",
        default=lambda self: self._get_default_release_note_version(),
        readonly=True,
    )
    has_unread_release_note = fields.Boolean(
        readonly=True, help="Whether the user has unread release notes."
    )
