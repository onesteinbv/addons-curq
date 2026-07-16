from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestRestrictedUser(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.role_manager = cls.env.ref("container_accessibility.role_manager")
        cls.group_erp_manager = cls.env.ref("base.group_erp_manager")
        cls.group_partner_manager = cls.env.ref("base.group_partner_manager")
        cls.group_restricted = cls.env.ref("container_accessibility.group_restricted")
        cls.restricted_user = cls.env["res.users"].create(
            {
                "name": "Restricted User",
                "login": "restricted_user",
                "role_id": cls.role_manager.id,
            }
        )
        cls.role_without_restricted_group = cls.env["res.users.role"].create(
            {
                "name": "Role Without Restricted Group",
                "implied_ids": [
                    Command.link(cls.group_erp_manager.id),
                    Command.link(cls.group_partner_manager.id),
                ],
            }
        )
        cls.admin = cls.env.ref("base.user_admin")
        cls.new_non_restricted_user = cls.env["res.users"].create(
            {
                "name": "New User",
                "login": "new_user",
                "role_id": cls.role_without_restricted_group.id,
            }
        )
        cls.new_restricted_user = cls.env["res.users"].create(
            {
                "name": "New Restricted User",
                "login": "new_restricted_user",
                "role_id": cls.role_manager.id,
            }
        )

    def test_cannot_create_non_restricted_user(self):
        with self.assertRaises(AccessError):
            self.env["res.users"].with_user(self.restricted_user).create(
                {
                    "name": "New User",
                    "login": "new_user_2",
                    "role_id": self.role_without_restricted_group.id,
                }
            )

        user = (
            self.env["res.users"]
            .with_user(self.restricted_user)
            .create(
                {
                    "name": "New User",
                    "login": "new_user_2",
                    "role_id": self.role_manager.id,
                }
            )
        )
        self.assertTrue(user.is_restricted_user())

    def test_cannot_write_non_restricted_user(self):
        # Test whether the user can change the groups of a non-restricted user
        with self.assertRaises(AccessError):
            self.new_non_restricted_user.with_user(self.restricted_user).write(
                {
                    "name": "Changed Name",
                }
            )

        # Test whether the user can make non-restricted user a restricted user
        with self.assertRaises(AccessError):
            self.admin.with_user(self.restricted_user).write(
                {"role_id": self.role_manager.id}
            )
        with self.assertRaises(AccessError):
            (self.admin + self.new_restricted_user).with_user(
                self.restricted_user
            ).write({"role_id": self.role_manager.id})

    def test_non_restricted_user_access(self):
        self.restricted_user.with_user(self.admin).write(
            {"role_id": self.role_without_restricted_group.id}
        )
        self.assertFalse(self.restricted_user.is_restricted_user())
        self.admin.write({"name": "Changed name"})
        new_user = (
            self.env["res.users"]
            .with_user(self.admin)
            .create(
                {
                    "name": "New User",
                    "login": "new_user_2",
                    "groups_id": [
                        self.group_erp_manager.id,
                        self.group_partner_manager.id,
                    ],
                }
            )
        )
        self.assertFalse(new_user.is_restricted_user())
