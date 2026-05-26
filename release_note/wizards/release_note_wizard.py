import logging
import re

import markdown

from odoo import api, fields, models
from odoo.tools import file_path

from ..utils import version_to_tuple

_logger = logging.getLogger(__name__)


class ReleaseNoteWizard(models.TransientModel):
    _name = "release.note.wizard"
    _description = "Release Notes"

    user_id = fields.Many2one(
        comodel_name="res.users", required=True, default=lambda self: self.env.user
    )
    include_read = fields.Boolean(default=False)
    news = fields.Html(compute="_compute_news", readonly=True)

    def _register_hook(self):
        super()._register_hook()
        release_notes = self._parse_release_notes()

        current_version = "0.0.0"
        project_name = "Odoo"
        if release_notes:
            # Find the latest version among the release notes
            last_release = max(
                release_notes, key=lambda note: version_to_tuple(note["version"])
            )
            current_version = last_release["version"]
            project_name = last_release["project"]

        # Store the version and project name in ir.config_parameter
        self.env["ir.config_parameter"].sudo().set_param(
            "release_note.current_version", current_version
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "release_note.project", project_name
        )

        version_tuple = version_to_tuple(current_version)

        # If the user has unread release notes, we want to show the wizard on startup, so we set the flag.
        for user in self.env["res.users"].search([]):
            # Make sure on installation we don't mark all release notes as unread for all users.
            if not user.last_release_note_version:
                user.last_release_note_version = current_version
            user.has_unread_release_note = (
                version_to_tuple(user.last_release_note_version) < version_tuple
            )

    @api.model
    def _get_release_notes_from_file(self):
        try:
            file_location = file_path("NEWS.md")
            return open(file_location, "r").read()
        except FileNotFoundError:
            _logger.warning("NEWS.md file not found.")
            return ""

    @api.model
    def _get_release_notes(self):
        """Override this method to change the source of the release notes.
        By default, it reads from a file
        """
        return self._get_release_notes_from_file()

    @api.model
    def _get_release_note_header_regex(self):
        """Override this method if your release note have a different format."""
        return r"^#\ (?P<project>.*?)\ (?P<version>[^\ ]+)\ \((?P<date>[^)]+)\)\s*\n(?P<content>.*?)(?=^#\ |\Z)"

    @api.model
    def _parse_release_notes(self):
        """Returns a list of dicts (project, version_tuple, version, date, content) for each release note."""
        release_note = self._get_release_notes()
        release_notes = []

        regex_expression = self._get_release_note_header_regex()
        matches = re.findall(regex_expression, release_note, re.DOTALL | re.MULTILINE)
        for match in matches:
            project, version, date, content = match
            release_notes.append(
                {
                    "project": project,
                    "version_tuple": version_to_tuple(version),
                    "version": version,
                    "date": date,
                    "content": markdown.markdown(content.strip()),
                }
            )
        return release_notes

    def _new_release_notes(self):
        """Returns the release notes that are new to the user."""
        self.ensure_one()
        all_release_notes = self._parse_release_notes()
        last_read_version = (0, 0, 0)
        if self.user_id.last_release_note_version:
            last_read_version = version_to_tuple(self.user_id.last_release_note_version)
        new_release_notes = [
            note
            for note in all_release_notes
            if note["version_tuple"] > last_read_version
        ]
        return new_release_notes

    @api.depends("user_id", "user_id.last_release_note_version", "include_read")
    def _compute_news(self):
        for wizard in self:
            new_release_notes = (
                wizard._parse_release_notes()
                if wizard.include_read
                else wizard._new_release_notes()
            )
            news_as_html = self.env["ir.qweb"]._render(
                "release_note.release_note_template", {"items": new_release_notes}
            )
            wizard.news = news_as_html

    @api.model
    def action_open_release_notes(self):
        """Open release notes wizard if there are unread release notes,
        otherwise do nothing.
        """
        user = self.env.user
        if not user.has_unread_release_note:
            return
        return self.env["ir.actions.act_window"]._for_xml_id(
            "release_note.release_note_wizard_action"
        )

    @api.model
    def mark_release_notes_as_read(self):
        """Mark the release notes as read for the current user."""
        current_version = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("release_note.current_version", default="0.0.0")
        )
        self.env.user.last_release_note_version = current_version
        self.env.user.has_unread_release_note = False
