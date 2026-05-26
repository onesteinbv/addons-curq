from os.path import dirname, join
from pathlib import Path
from unittest.mock import patch

from odoo.tests import common

from odoo.addons.release_note.wizards.release_note_wizard import ReleaseNoteWizard


class TestReleaseNote(common.TransactionCase):
    @classmethod
    def _read_fixture(cls, filename):
        data_dir = Path(join(dirname(__file__), "fixtures"))
        return (data_dir / filename).read_text()

    def test_empty_news_file(self):
        fixture_content = self._read_fixture("NEWS-empty.md")

        with patch.object(
            ReleaseNoteWizard, "_get_release_notes", return_value=fixture_content
        ):
            parsed = self.env["release.note.wizard"]._parse_release_notes()

        self.assertEqual(parsed, [])

    def test_malformed_news_file(self):
        """If the NEWS file is malformated, we don't want the system to crash,
        but simply consider that there is no release note to show."""
        fixture_content = self._read_fixture("NEWS-malformated.md")

        with patch.object(
            ReleaseNoteWizard, "_get_release_notes", return_value=fixture_content
        ):
            parsed = self.env["release.note.wizard"]._parse_release_notes()

        self.assertEqual(parsed, [])

    def test_different_versioning_no_error(self):
        fixture_content = self._read_fixture("NEWS-version-variants.md")

        with patch.object(
            ReleaseNoteWizard, "_get_release_notes", return_value=fixture_content
        ):
            parsed = self.env["release.note.wizard"]._parse_release_notes()

        self.assertEqual(len(parsed), 3)
        self.assertEqual([note["version"] for note in parsed], ["v1.2.3", "1.2", "1"])

    def test_mixed_version_length(self):
        fixture_content = self._read_fixture("NEWS-version-variants.md")
        user = self.env.ref("base.user_demo")
        user.last_release_note_version = "1.1"
        wizard = self.env["release.note.wizard"].create({"user_id": user.id})

        with patch.object(
            ReleaseNoteWizard, "_get_release_notes", return_value=fixture_content
        ):
            new_notes = wizard._new_release_notes()

        self.assertEqual([note["version"] for note in new_notes], ["v1.2.3", "1.2"])

    def test_news_is_unordered(self):
        """Allow NEWS file to be unordered for flexibility"""
        fixture_content = self._read_fixture("NEWS-unordered.md")

        with patch.object(
            ReleaseNoteWizard, "_get_release_notes", return_value=fixture_content
        ):
            self.env["release.note.wizard"]._register_hook()

        current_version = self.env["ir.config_parameter"].get_param(
            "release_note.current_version", default="0.0.0"
        )
        self.assertEqual(current_version, "19.0.1")

    def test_new_user(self):
        """Test that a new user (without last_release_note_version) is considered to have read the
        current version, to avoid overwhelming them with old release notes.
        """
        current_version = "18.0.9"
        self.env["ir.config_parameter"].set_param(
            "release_note.current_version", current_version
        )

        user = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "Release Note New User",
                    "login": "release_note_new_user",
                }
            )
        )

        self.assertEqual(user.last_release_note_version, current_version)

    def test_logs_when_news_file_missing(self):
        logger_name = "odoo.addons.release_note.wizards.release_note_wizard"

        with self.assertLogs(logger_name, level="WARNING"):
            with patch(
                "odoo.addons.release_note.wizards.release_note_wizard.file_path",
                side_effect=FileNotFoundError,
            ):
                content = self.env["release.note.wizard"]._get_release_notes_from_file()

        self.assertEqual(content, "")
