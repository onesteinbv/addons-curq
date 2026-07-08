from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestUserRole(TransactionCase):
    def _new_group(self, name, xml_id):
        new_group = self.env["res.groups"].create(
            {
                "name": name,
            }
        )
        module, name = xml_id.split(".")
        data = self.env["ir.model.data"].create(
            {
                "name": name,
                "model": "res.groups",
                "res_id": new_group.id,
                "module": module,
            }
        )
        return new_group, data

    def test_implied_by_text(self):
        groups = self.env.ref("base.group_system") + self.env.ref(
            "container_accessibility.group_restricted"
        )
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )

        self.assertEqual(role.implied_ids, groups)

    def test_implied_by_text_with_non_existing_group(self):
        groups = self.env.ref("base.group_system") + self.env.ref(
            "container_accessibility.group_restricted"
        )
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )

        self.assertEqual(role.implied_ids, groups)

        role.invalidate_recordset()

        # Implied by text should still contain the non existing group
        self.assertEqual(role.implied_by_text, group_xml_ids)

    def test_new_group(self):
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )
        new_group, _ = self._new_group(
            "New Group", "container_accessibility.group_non_existing"
        )
        self.assertEqual(
            self.ref("container_accessibility.group_non_existing"), new_group.id
        )
        self.assertIn(new_group, role.implied_ids)

    def test_delete_data(self):
        new_group, data = self._new_group(
            "New Group", "container_accessibility.group_non_existing"
        )
        new_group_2, data_2 = self._new_group(
            "New Group", "container_accessibility.group_non_existing_2"
        )
        new_group_3, data_3 = self._new_group(
            "New Group", "container_accessibility.group_non_existing_3"
        )

        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing\ncontainer_accessibility.group_non_existing_2\ncontainer_accessibility.group_non_existing_3"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )
        self.assertIn(new_group, role.implied_ids)
        self.assertIn(new_group_2, role.implied_ids)
        self.assertIn(new_group_3, role.implied_ids)

        data.unlink()
        self.assertNotIn(new_group, role.implied_ids)
        self.assertIn(new_group_2, role.implied_ids)
        self.assertIn(new_group_3, role.implied_ids)

        (data_2 + data_3).unlink()
        self.assertNotIn(new_group_2, role.implied_ids)
        self.assertNotIn(new_group_3, role.implied_ids)

    def test_xml_id_changed(self):
        new_group, data = self._new_group(
            "New Group", "container_accessibility.group_non_existing"
        )
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )
        self.assertIn(new_group, role.implied_ids)

        data.name = "group_non_existing_renamed"
        self.assertNotIn(new_group, role.implied_ids)

    def test_inverse_role_id(self):
        manager_role = self.ref("container_accessibility.role_manager")
        user_role = self.ref("container_accessibility.role_user")
        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "testuser",
                "role_id": manager_role,
            }
        )
        self.assertEqual(user.role_id.id, manager_role)
        self.assertEqual(user.role_line_ids.role_id.id, manager_role)
        user.role_id = user_role
        self.assertEqual(user.role_id.id, user_role)
        self.assertEqual(len(user.role_line_ids), 1)
        self.assertEqual(user.role_line_ids.role_id.id, user_role)

    def test_role_id_required_for_restricted_group(self):
        group_erp_manager = self.env.ref("base.group_erp_manager")
        group_restricted = self.env.ref("container_accessibility.group_restricted")
        group_contact_creation = self.env.ref("base.group_partner_manager")

        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "testuser",
                "groups_id": (
                    group_erp_manager + group_restricted + group_contact_creation
                ),
            }
        )

        with self.assertRaisesRegex(ValidationError, "must have a role assigned"):
            self.env["res.users"].with_user(user).create(
                {
                    "name": "Another Test User",
                    "login": "anothertestuser",
                }
            )

        new_user = self.env["res.users"].create(
            {
                "name": "Another Test User",
                "login": "anothertestuser",
                "role_id": self.ref("container_accessibility.role_user"),
            }
        )
        with self.assertRaisesRegex(ValidationError, "must have a role assigned"):
            new_user.with_user(user).write({"role_id": False})

    def test_role_id_optional_for_non_restricted_group(self):
        user = self.env.ref("base.user_admin")

        self.env["res.users"].with_user(user).create(
            {
                "name": "Another Test User",
                "login": "anothertestuser",
            }
        )

    def test_role_copied_to_new_user(self):
        manager_role = self.ref("container_accessibility.role_manager")
        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "testuser",
                "role_id": manager_role,
            }
        )
        new_user = user.copy(
            {
                "name": "Copied User",
                "login": "copieduser",
            }
        )
        self.assertEqual(new_user.role_id.id, manager_role)
        self.assertEqual(len(new_user.role_line_ids), 1)
        self.assertEqual(new_user.role_line_ids.role_id.id, manager_role)

    def test_guest_role(self):
        """Test wether the guest role is a shared user and isn't an internal user"""
        group_user = self.ref("base.group_user")
        group_portal = self.ref("base.group_portal")
        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "testuser",
                "role_id": self.ref("container_accessibility.role_guest"),
            }
        )
        self.assertIn(group_portal, user.groups_id.ids)
        self.assertNotIn(group_user, user.groups_id.ids)
        self.assertTrue(user.share, "Guest role should be a shared user")

    def test_portal_grant_access_wizard(self):
        """Test that the portal wizard grants assigns the guest role when granting access to a partner."""
        partner = self.env.ref("base.res_partner_address_4")
        wizard = (
            self.env["portal.wizard"].with_context(active_ids=[partner.id]).create({})
        )
        wizard.user_ids.action_grant_access()
        partner.user_ids.ensure_one()
        self.assertEqual(
            partner.user_ids.role_id.id, self.ref("container_accessibility.role_guest")
        )

    def test_restricted_user_cannot_remove_role(self):
        """Test that a restricted user cannot remove the role of another user."""
        role_user = self.ref("container_accessibility.role_user")
        role_admin = self.ref("container_accessibility.role_administrator")
        restricted_admin = self.env["res.users"].create(
            {
                "name": "Restricted Admin",
                "login": "restrictedadmin",
                "role_id": role_admin,
            }
        )
        other_user = self.env["res.users"].create(
            {
                "name": "Other User",
                "login": "otheruser",
                "role_id": role_user,
            }
        )
        with self.assertRaisesRegex(
            ValidationError,
            "Users must have a role assigned. Please assign a role to the user and try again.",
        ):
            other_user.with_user(restricted_admin).write({"role_id": False})
        self.assertEqual(other_user.role_id.id, role_user)
        self.assertTrue(other_user.is_restricted_user())
        # Test that a restricted user cannot remove their own role
        with self.assertRaisesRegex(
            ValidationError,
            "Users must have a role assigned. Please assign a role to the user and try again.",
        ):
            restricted_admin.with_user(restricted_admin).write({"role_id": False})
        self.assertEqual(restricted_admin.role_id.id, role_admin)
        self.assertTrue(restricted_admin.is_restricted_user())
