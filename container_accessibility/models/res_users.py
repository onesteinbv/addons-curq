from lxml import etree

from odoo import Command, _, api, models
from odoo.exceptions import AccessError, UserError
from odoo.osv import expression
from odoo.tools import config
from odoo.tools.misc import ustr

from odoo.addons.auth_signup.models.res_users import SignupError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _get_user_limit(self):
        return int(config.get("user_limit", "0"))

    @api.model
    def _get_limit_included_user_count(self):
        restricted_group = self.env.ref("container_accessibility.group_restricted")
        count = self.search([("groups_id", "in", restricted_group.ids)], count=True)
        return count

    def _check_user_limit_exceeded(self):
        user_count = self._get_limit_included_user_count()
        if user_count > self._get_user_limit():
            raise UserError(_("User limit exceeded"))

    @api.model
    def _get_forced_groups(self):
        return ["container_accessibility.group_restricted"]

    def is_restricted_user(self):
        self.ensure_one()
        return self.has_group("container_accessibility.group_restricted")

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        allow_override = not self.env.user.is_restricted_user()
        if view_type == "form" and not allow_override:
            forced_groups = self._get_forced_groups()
            for group in forced_groups:
                erp_group_id = self.env.ref(group).id
                sel_xpath = (
                    "//field[contains(@name, 'sel_groups_%s_')]/.." % erp_group_id
                )
                in_xpath = "//field[@name='in_group_%s']" % erp_group_id
                xml = etree.XML(res["arch"])
                xml_groups = xml.xpath(sel_xpath) + xml.xpath(in_xpath)
                for xml_group in xml_groups:
                    xml_group.getparent().remove(xml_group)
                res["arch"] = etree.tostring(xml, encoding="unicode")
        return res

    def _force_groups(self):
        allow_override = not self.env.user.is_restricted_user()
        if allow_override:
            return
        forced_groups = self._get_forced_groups()
        for user in self.filtered(lambda u: u._is_internal()):
            for group in forced_groups:
                if user.has_group(group):
                    continue
                group_record = self.env.ref(group)
                user.sudo().write({"groups_id": [Command.link(group_record.id)]})

    def write(self, vals):
        # FIXME: Quickfix, somewhere in super().create() another module writes the record.
        #  This should be fixed in create() but as there's a time limit i've done it like this
        #  you know how it goes sometimes
        if not self.env.su:
            self._force_groups()
        res = super().write(vals)
        # Disallow changing default access rights (for now)
        # Changing groups in the default_user will change the groups in all internal users
        if (
            self.env.ref("base.default_user") in self
            and self.env.user.is_restricted_user()
        ):
            raise AccessError(_("Access denied to change default user"))
        if not self.env.su:
            self._force_groups()
        if (
            "active" in vals and vals["active"] and self._get_user_limit()
        ):  # If trying to activate / unarchive a user
            self._check_user_limit_exceeded()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if not self.env.su:
            res._force_groups()
        if self._get_user_limit():
            self._check_user_limit_exceeded()
        return res

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        # Purely for UX purposes
        model = self.with_user(access_rights_uid) if access_rights_uid else self
        if model.env.user.is_restricted_user() and not self.env.su:
            args = expression.AND(
                [
                    args,
                    [
                        "|",
                        ("share", "=", True),
                        (
                            "groups_id",
                            "in",
                            self.env.ref(
                                "container_accessibility.group_restricted"
                            ).ids,
                        ),
                    ],
                ]
            )

        return super()._search(args, offset, limit, order, count, access_rights_uid)

    def _create_user_from_template(self, values):
        # Maybe: inherit get_param (ir.config_parameter) instead because this is much redundancy 🤢
        if values.get("oauth_provider_id", False):
            provider_record = (
                self.env["auth.oauth.provider"]
                .sudo()
                .browse(values["oauth_provider_id"])
            )
            if not provider_record.private:
                return super()._create_user_from_template(values)

            template_user = provider_record.template_user_id or self.env.ref(
                "base.template_portal_user_id"
            )
            if not values.get("login"):
                raise ValueError(_("Signup: no login given for new user"))
            if not values.get("partner_id") and not values.get("name"):
                raise ValueError(_("Signup: no name or partner given for new user"))
            values["active"] = True
            try:
                with self.env.cr.savepoint():
                    new_user = template_user.with_context(no_reset_password=True).copy(
                        values
                    )
                    new_user.groups_id += provider_record.group_ids
                    return new_user
            except Exception as e:
                raise SignupError(ustr(e)) from e
        return super()._create_user_from_template(values)

    @api.model
    def _signup_create_user(self, values):
        if values.get("oauth_provider_id", False):
            provider_record = (
                self.env["auth.oauth.provider"]
                .sudo()
                .browse(values["oauth_provider_id"])
            )
            if provider_record.private:
                return self._create_user_from_template(values)

        return super()._signup_create_user(values)
