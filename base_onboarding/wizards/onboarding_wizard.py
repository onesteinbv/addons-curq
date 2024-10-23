from odoo import _, api, fields, models


class OnboardingWizard(models.TransientModel):
    _name = "base.onboarding.wizard"
    _inherit = ["multi.step.wizard.mixin"]
    _description = "Onboarding Wizard"

    company_id = fields.Many2one(
        comodel_name="res.company", default=lambda self: self.env.company
    )
    company_logo = fields.Binary(related="company_id.logo", readonly=False)
    company_vat = fields.Char(related="company_id.vat", readonly=False)
    company_registry = fields.Char(
        related="company_id.company_registry", readonly=False
    )
    company_phone = fields.Char(related="company_id.phone", readonly=False)
    company_email = fields.Char(related="company_id.email", readonly=False)
    company_website = fields.Char(related="company_id.website", readonly=False)

    fetchmail_server_id = fields.Many2one(
        comodel_name="fetchmail.server", string="Incoming Mail Server"
    )
    ir_mail_server_id = fields.Many2one(
        comodel_name="ir.mail_server", string="Outgoing Mail Server"
    )

    module_ids = fields.Many2many(
        comodel_name="ir.module.module", compute="_compute_module_ids"
    )

    @api.depends("state")
    def _compute_module_ids(self):
        installable_module_names = [
            "account_install",
            "website_install",
            "membership_install",
            "hr_install",
        ]
        installable_modules = self.env["ir.module.module"].search(
            [("name", "in", installable_module_names)]
        )
        for wizard in self:
            wizard.module_ids = installable_modules

    @api.depends("state")
    def _compute_allow_back(self):
        for record in self:
            record.allow_back = record.state != "start"

    def _reopen_self(self):
        action = super()._reopen_self()
        action["name"] = _("Welcome to Odoo")
        return action

    @api.model
    def _selection_state(self):
        return [
            ("start", "Installation"),
            ("company_info", "Company Information"),
            ("mailing", "Mailing"),
            ("final", "Final"),
        ]

    def _get_current_state_index(self):
        state_selection = self._selection_state()
        state_index = 0
        for state in state_selection:
            if self.state == state[0]:
                break
            state_index += 1
        return state_index

    def _get_next_state(self):
        state_selection = self._selection_state()
        state_index = self._get_current_state_index()
        return state_selection[state_index + 1][0]

    def _get_previous_state(self):
        state_selection = self._selection_state()
        state_index = self._get_current_state_index()
        return state_selection[state_index - 1][0]

    def go_to_state(self, state):
        self.state = state
        enter_method = getattr(self, "state_enter_{}".format(self.state), None)
        if enter_method:
            enter_method()
        return self._reopen_self()

    def open_next(self):
        state_method = getattr(self, "state_exit_{}".format(self.state), None)
        if state_method is None:
            return self.go_to_state(self._get_next_state())
        return super().open_next()

    def open_previous(self):
        state_method = getattr(self, "state_previous_{}".format(self.state), None)
        if state_method is None:
            return self.go_to_state(self._get_previous_state())
        return super().open_previous()

    def state_exit_start(self):
        return self.go_to_state(self._get_next_state())

    def state_enter_final(self):
        onboarding_group = self.env.ref("base_onboarding.onboarding_group")
        onboarding_group.sudo().write({"users": [(3, self.env.user.id, 0)]})

    def skip_to_end(self):
        self.ensure_one()
        return self.go_to_state("final")
