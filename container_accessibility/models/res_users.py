from lxml import etree

from odoo import Command, _, api, models
from odoo.exceptions import UserError
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
        count = self.search(
            [("share", "=", False), ("groups_id", "in", restricted_group.ids)],
            count=True,
        )
        return count

    def _check_user_limit_exceeded(self):
        user_count = self._get_limit_included_user_count()
        if user_count > self._get_user_limit():
            raise UserError(_("User limit exceeded"))

    def is_restricted_user(self):
        self.ensure_one()
        return self.has_group("container_accessibility.group_restricted")

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """
        Remove groups (just container_accessibility.group_restricted atm) from the form view for ux
        """
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        is_restricted = self.env.user.is_restricted_user()
        if view_type == "form" and is_restricted:
            group_restricted_id = self.env.ref(
                "container_accessibility.group_restricted"
            ).id
            sel_xpath = (
                "//field[contains(@name, 'sel_groups_%s_')]/.." % group_restricted_id
            )
            in_xpath = "//field[@name='in_group_%s']" % group_restricted_id
            xml = etree.XML(res["arch"])
            xml_groups = xml.xpath(sel_xpath) + xml.xpath(in_xpath)
            for xml_group in xml_groups:
                xml_group.getparent().remove(xml_group)
            res["arch"] = etree.tostring(xml, encoding="unicode")
        return res

    def write(self, vals):
        is_restricted = self.env.user.is_restricted_user()
        user_type_category = self.env.ref("base.module_category_user_type")
        user_type_groups = self.env["res.groups"].search(
            [("category_id", "=", user_type_category.id)]
        )
        user_type_reified_field = "sel_groups_%s" % (
            "_".join(str(gid) for gid in user_type_groups.ids)
        )

        # Automatically add the restricted group for ux
        if is_restricted:
            group_restricted = self.env.ref("container_accessibility.group_restricted")
            group_user = self.env.ref("base.group_user")
            restricted_reified_field = "in_group_%s" % group_restricted.id

            internal_user = (
                vals.get(user_type_reified_field, group_user.id) == group_user.id
            )
            if internal_user:
                vals[restricted_reified_field] = True

        # The record rule doesn't care if the record was restricted before
        # Prevents the current becoming non-restricted
        keep_restricted = self.filtered(lambda u: u.is_restricted_user())
        res = super().write(vals)
        forbidden_users = self.filtered(
            lambda u: not u.share
            and u in keep_restricted
            and not u.is_restricted_user()
        )
        if is_restricted and forbidden_users:
            forbidden_users.write(
                {
                    "groups_id": [
                        Command.link(
                            self.env.ref("container_accessibility.group_restricted").id
                        )
                    ]
                }
            )

        # When trying to activate / un-archive a user we should check the limit, or when changing the user type
        if (
            "active" in vals
            and vals["active"]
            or "group_ids" in vals
            or user_type_reified_field in vals
        ) and self._get_user_limit():
            self._check_user_limit_exceeded()

        return res

    @api.model_create_multi
    def create(self, vals_list):
        # Automatically add the restricted group for ux
        if self.env.user.is_restricted_user():
            group_restricted = self.env.ref("container_accessibility.group_restricted")
            group_user = self.env.ref("base.group_user")
            user_type_category = self.env.ref("base.module_category_user_type")
            user_type_groups = self.env["res.groups"].search(
                [("category_id", "=", user_type_category.id)]
            )

            restricted_reified_field = "in_group_%s" % group_restricted.id
            user_type_reified_field = "sel_groups_%s" % (
                "_".join(str(gid) for gid in user_type_groups.ids)
            )

            for vals in vals_list:
                internal_user = (
                    vals.get(user_type_reified_field, group_user.id) == group_user.id
                )
                if internal_user:
                    vals[restricted_reified_field] = True

        res = super().create(vals_list)
        if self._get_user_limit():
            self._check_user_limit_exceeded()
        return res

    def _create_user_from_template(self, values):
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
