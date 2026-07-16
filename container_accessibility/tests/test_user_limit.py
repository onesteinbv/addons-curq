from contextlib import contextmanager
from unittest.mock import patch

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestUserLimit(TransactionCase):
    @contextmanager
    def _mock_user_limit(self, limit):
        with patch(
            "odoo.addons.container_accessibility.models.res_users.ResUsers._get_user_limit",
            return_value=limit,
        ):
            yield

    def test_no_user_limit(self):
        """Should never be called if user limit is 0 (unlimited)"""
        with (
            self._mock_user_limit(0),
            patch(
                "odoo.addons.container_accessibility.models.res_users.ResUsers._get_limit_included_user_count"
            ) as _get_limit_included_user_count,
        ):
            new_user = self.env["res.users"].create(
                {"name": "Test User", "login": "testuser"}
            )
            new_user.groups_id = [
                (4, self.ref("container_accessibility.group_restricted"))
            ]
            _get_limit_included_user_count.assert_not_called()

    def test_user_limit_exceeded(self):
        """Should raise UserError if user limit is exceeded"""
        current_count = self.env["res.users"]._get_limit_included_user_count()
        role_user = self.ref("container_accessibility.role_user")
        role_manager = self.ref("container_accessibility.role_manager")
        role_administrator = self.ref("container_accessibility.role_administrator")
        with self._mock_user_limit(current_count + 1):
            with patch(
                "odoo.addons.container_accessibility.models.res_users.ResUsers._get_limit_included_user_count",
                return_value=current_count,
            ) as _get_limit_included_user_count:
                new_user = self.env["res.users"].create(
                    {"name": "Test User", "login": "testuser", "role_id": role_user}
                )
                _get_limit_included_user_count.assert_called()
            with patch(
                "odoo.addons.container_accessibility.models.res_users.ResUsers._get_limit_included_user_count",
                return_value=current_count + 1,
            ) as _get_limit_included_user_count:
                new_user.role_id = role_manager
                _get_limit_included_user_count.assert_called()
            user_count = self.env["res.users"]._get_limit_included_user_count()
            with self.assertRaisesRegex(ValidationError, "User limit exceeded"):
                self.env["res.users"].create(
                    {
                        "name": "Test User2",
                        "login": "testuser2",
                        "role_id": role_user,
                    }
                )
            new_user_count = self.env["res.users"]._get_limit_included_user_count()
            self.assertEqual(
                user_count, new_user_count, "User count should not have changed"
            )

            new_user_administrator = self.env["res.users"].create(
                {
                    "name": "Test User3",
                    "login": "testuser3",
                    "role_id": role_administrator,
                }
            )
            with self.assertRaisesRegex(ValidationError, "User limit exceeded"):
                new_user_administrator.role_id = role_manager
            self.assertEqual(new_user_administrator.role_id.id, role_administrator)

    def test_multi_write_user_limit_exceeded(self):
        """Should raise UserError if user limit is exceeded when writing multiple users"""
        current_count = self.env["res.users"]._get_limit_included_user_count()
        role_user = self.ref("container_accessibility.role_user")
        role_manager = self.ref("container_accessibility.role_manager")
        role_administrator = self.ref("container_accessibility.role_administrator")

        # Test that writing multiple users to a role that is included in the user limit raises a
        # ValidationError if the limit is exceeded
        with self._mock_user_limit(current_count + 1):
            new_user1 = self.env["res.users"].create(
                {"name": "Test User1", "login": "testuser1", "role_id": role_manager}
            )
            new_user2 = self.env["res.users"].create(
                {
                    "name": "Test User2",
                    "login": "testuser2",
                    "role_id": role_administrator,
                }
            )
            with self.assertRaisesRegex(ValidationError, "User limit exceeded"):
                (new_user1 + new_user2).write({"role_id": role_user})

        self.assertEqual(
            current_count + 1,
            self.env["res.users"]._get_limit_included_user_count(),
            "User count only be increased by 1 since only one user was changed to a role that is included in the user limit",
        )

        # Multi-write from included role to included role should be allowed if user limit is not exceeded
        current_count = self.env["res.users"]._get_limit_included_user_count()
        with self._mock_user_limit(current_count + 2):
            new_user1 = self.env["res.users"].create(
                {"name": "Test User3", "login": "testuser3", "role_id": role_manager}
            )
            new_user2 = self.env["res.users"].create(
                {"name": "Test User4", "login": "testuser4", "role_id": role_manager}
            )
            (new_user1 + new_user2).write({"role_id": role_user})
            self.assertEqual(new_user1.role_id.id, role_user)
            self.assertEqual(new_user2.role_id.id, role_user)

    def test_multi_create_user_limit_exceeded(self):
        current_count = self.env["res.users"]._get_limit_included_user_count()
        role_manager = self.ref("container_accessibility.role_manager")
        with self._mock_user_limit(current_count + 1):
            with self.assertRaisesRegex(ValidationError, "User limit exceeded"):
                self.env["res.users"].create(
                    [
                        {
                            "name": "Test User1",
                            "login": "testuser1",
                            "role_id": role_manager,
                        },
                        {
                            "name": "Test User2",
                            "login": "testuser2",
                            "role_id": role_manager,
                        },
                    ]
                )

    def test_correct_user_limit_count(self):
        """Archived users should not be counted towards the user limit, only users in role_manager, role_user, role_accountant role."""
        current_count = self.env["res.users"]._get_limit_included_user_count()
        new_user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "testuser",
                "role_id": self.ref("container_accessibility.role_user"),
                "active": False,
            }
        )
        new_count = self.env["res.users"]._get_limit_included_user_count()
        self.assertEqual(
            current_count,
            new_count,
            "Inactive users should not be counted towards the user limit.",
        )
        new_user.active = True
        new_count = self.env["res.users"]._get_limit_included_user_count()
        self.assertEqual(
            current_count + 1,
            new_count,
            "Active users in role_user should be counted towards the user limit.",
        )
        current_count = self.env["res.users"]._get_limit_included_user_count()
        new_user.role_id = self.ref("container_accessibility.role_administrator")
        new_count = self.env["res.users"]._get_limit_included_user_count()
        self.assertEqual(
            current_count - 1,
            new_count,
            "role_administrator should not be counted towards the user limit.",
        )
