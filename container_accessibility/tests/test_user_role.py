from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase


class TestUserRole(TransactionCase):
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

    def test_administrator_can_assign_administrator(self):
        """Administrators should be able to assign the administrator role to itself and other users."""
        role_admin = self.ref("container_accessibility.role_administrator")
        role_user = self.ref("container_accessibility.role_user")
        user_admin = self.env["res.users"].create(
            {
                "name": "Administrator User",
                "login": "administratoruser",
                "role_id": role_admin,
            }
        )
        user_other = self.env["res.users"].create(
            {
                "name": "Other User",
                "login": "otheruser",
                "role_id": role_user,
            }
        )
        # Test that an administrator can assign the administrator role to itself
        user_admin.with_user(user_admin).write({"role_id": role_admin})
        self.assertEqual(user_admin.role_id.id, role_admin)

        # Test that an administrator can assign the administrator role to another user
        user_other.with_user(user_admin).write({"role_id": role_admin})
        self.assertEqual(user_other.role_id.id, role_admin)

    def test_manager_cannot_assign_administrator(self):
        """Managers should not be able to assign the administrator role to itself and other users."""
        role_accountant = self.ref("container_accessibility.role_accountant")
        role_admin = self.ref("container_accessibility.role_administrator")
        role_manager = self.ref("container_accessibility.role_manager")
        user_manager = self.env["res.users"].create(
            {
                "name": "Manager User",
                "login": "manageruser",
                "role_id": role_manager,
            }
        )
        user_accountant = self.env["res.users"].create(
            {
                "name": "Other User",
                "login": "otheruser",
                "role_id": role_accountant,
            }
        )
        real_admin = self.env.ref("base.user_admin")

        # Test that a manager cannot assign the administrator role to itself
        with self.assertRaises(AccessError):
            user_manager.with_user(user_manager).write({"role_id": role_admin})
        self.assertEqual(user_manager.role_id.id, role_manager)

        # Test a manager cannot assign the administrator role to another user
        with self.assertRaises(AccessError):
            user_accountant.with_user(user_manager).write({"role_id": role_admin})

        # Test that a manager can assign the manager role to another user
        user_accountant.with_user(user_manager).write({"role_id": role_manager})
        self.assertEqual(user_accountant.role_id.id, role_manager)
        user_accountant.with_user(user_manager).write({"role_id": role_accountant})
        self.assertEqual(user_accountant.role_id.id, role_accountant)

        # Test cannot create a user with the administrator role
        with self.assertRaises(AccessError):
            self.env["res.users"].with_user(user_manager).create(
                {
                    "name": "New User",
                    "login": "newuser",
                    "role_id": role_admin,
                }
            )

        # Test cannot touch a user without role
        with self.assertRaises(AccessError):
            real_admin.with_user(user_manager).write({"role_id": role_admin})

    def test_manager_cannot_crud_administrator(self):
        """Managers should not be able to crud users with the administrator role."""
        role_manager = self.ref("container_accessibility.role_manager")
        role_admin = self.ref("container_accessibility.role_administrator")
        user_manager = self.env["res.users"].create(
            {
                "name": "Manager User",
                "login": "manageruser",
                "role_id": role_manager,
            }
        )
        user_admin = self.env["res.users"].create(
            {
                "name": "Admin User",
                "login": "adminuser",
                "role_id": role_admin,
            }
        )
        # Test that a manager cannot read a user with the administrator role
        with self.assertRaises(AccessError):
            self.env["res.users"].with_user(user_manager).browse(user_admin.id).read()
        # Test that a manager cannot write a user with the administrator role
        with self.assertRaises(AccessError):
            user_admin.with_user(user_manager).write({"name": "New Name"})
        self.assertEqual(user_admin.name, "Admin User")
        # Test that a manager cannot delete a user with the administrator role
        with self.assertRaises(AccessError):
            user_admin.with_user(user_manager).unlink()
        # Test that a manager cannot create a user with the administrator role
        with self.assertRaises(AccessError):
            self.env["res.users"].with_user(user_manager).create(
                {
                    "name": "New User",
                    "login": "newuser",
                    "role_id": role_admin,
                }
            )

    def test_administrator_role_not_listed_for_manager(self):
        """Test that the administrator role is not listed for a manager user."""
        role_manager = self.ref("container_accessibility.role_manager")
        role_admin = self.ref("container_accessibility.role_administrator")
        user_manager = self.env["res.users"].create(
            {
                "name": "Manager User",
                "login": "manageruser",
                "role_id": role_manager,
            }
        )
        roles = self.env["res.users.role"].with_user(user_manager).search([])
        self.assertNotIn(role_admin, roles.ids)

    def test_administrator_role_listed_for_administrator(self):
        """Test that the administrator role is listed for an administrator user."""
        role_admin = self.ref("container_accessibility.role_administrator")
        user_admin = self.env["res.users"].create(
            {
                "name": "Admin User",
                "login": "adminuser",
                "role_id": role_admin,
            }
        )
        roles = self.env["res.users.role"].with_user(user_admin).search([])
        self.assertIn(role_admin, roles.ids)

    def test_administrator_listed_for_administrator(self):
        """Test that the administrators are listed for an administrator user."""
        role_admin = self.ref("container_accessibility.role_administrator")
        user_admin = self.env["res.users"].create(
            {
                "name": "Admin User",
                "login": "adminuser",
                "role_id": role_admin,
            }
        )
        other_admin = self.env["res.users"].create(
            {
                "name": "Admin User",
                "login": "otheradminuser",
                "role_id": role_admin,
            }
        )
        users = self.env["res.users"].with_user(user_admin).search([])
        self.assertIn(user_admin.id, users.ids)
        self.assertIn(other_admin.id, users.ids)

    def test_crud_role(self):
        role_admin = self.ref("container_accessibility.role_administrator")
        role_user = self.ref("container_accessibility.role_user")
        user_admin = self.env["res.users"].create(
            {
                "name": "Admin User",
                "login": "adminuser",
                "role_id": role_admin,
            }
        )
        real_admin = self.env.ref("base.user_admin")
        # Test restricted user cannot create a role
        with self.assertRaises(AccessError):
            self.env["res.users.role"].with_user(user_admin).create(
                {
                    "name": "New Role",
                }
            )
        # Test restricted user cannot write a role
        with self.assertRaises(AccessError):
            role_user.with_user(user_admin).write(
                {
                    "name": "Updated Role",
                }
            )

        # Test restricted user cannot unlink a role
        with self.assertRaises(AccessError):
            role_user.with_user(user_admin).unlink()

        # Test non-restricted user can create a role
        role_new = (
            self.env["res.users.role"]
            .with_user(real_admin)
            .create(
                {
                    "name": "New role",
                }
            )
        )
        role_new.with_user(real_admin).write(
            {
                "name": "Updated New role",
            }
        )
        role_new.with_user(real_admin).unlink()
