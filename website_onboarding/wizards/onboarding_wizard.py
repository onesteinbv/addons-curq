from odoo import api, fields, models


class OnboardingWizard(models.TransientModel):
    _inherit = "base.onboarding.wizard"

    def _default_website(self):
        website = self.env["website"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )
        if (
            not website
        ):  # Get the first available website if there's no website found for the current active company
            website = self.env["website"].search([], limit=1)
        return website

    website_id = fields.Many2one(comodel_name="website", default=_default_website)
    website_name = fields.Char(related="website_id.name", readonly=False)

    social_twitter = fields.Char(related="website_id.social_twitter", readonly=False)
    social_facebook = fields.Char(related="website_id.social_facebook", readonly=False)
    social_linkedin = fields.Char(related="website_id.social_linkedin", readonly=False)
    social_youtube = fields.Char(related="website_id.social_youtube", readonly=False)
    social_instagram = fields.Char(
        related="website_id.social_instagram", readonly=False
    )
    theme_module_ids = fields.Many2many(
        comodel_name="ir.module.module", compute="_compute_theme_module_ids"
    )

    def _compute_theme_module_ids(self):
        for wizard in self:
            wizard.theme_module_ids = self.env["ir.module.module"].search(
                [
                    ("state", "!=", "uninstallable"),
                    (
                        "category_id",
                        "not in",
                        [
                            self.env["ir.model.data"]._xmlid_to_res_id(
                                "base.module_category_hidden"
                            ),
                            self.env["ir.model.data"]._xmlid_to_res_id(
                                "base.module_category_theme_hidden"
                            ),
                        ],
                    ),
                    "|",
                    (
                        "category_id",
                        "=",
                        self.env["ir.model.data"]._xmlid_to_res_id(
                            "base.module_category_theme"
                        ),
                    ),
                    (
                        "category_id.parent_id",
                        "=",
                        self.env["ir.model.data"]._xmlid_to_res_id(
                            "base.module_category_theme"
                        ),
                    ),
                ]
            )

    @api.model
    def _selection_state(self):
        selection = super()._selection_state()
        selection.insert(2, ("theme", "Theme"))
        selection.insert(2, ("website", "Website"))
        return selection
