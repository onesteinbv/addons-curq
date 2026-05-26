from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    release_note_version = fields.Char(
        string="Current Version",
        readonly=True,
        config_parameter="release_note.current_version",
    )
    release_note_project = fields.Char(
        readonly=True,
        config_parameter="release_note.project",
    )
