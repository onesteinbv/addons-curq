from contextlib import contextmanager
from unittest.mock import patch

from odoo.exceptions import UserError
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
                "odoo.addons.container_accessibility.models.res_users.ResUsers._check_user_limit_exceeded"
            ) as _check_user_limit_exceeded,
        ):
            new_user = self.env["res.users"].create(
                {"name": "Test User", "login": "testuser"}
            )
            new_user.groups_id = [
                (4, self.ref("container_accessibility.group_restricted"))
            ]
            _check_user_limit_exceeded.assert_not_called()

    def test_user_limit_exceeded(self):
        """Should raise UserError if user limit is exceeded"""
        current_count = self.env["res.users"]._get_limit_included_user_count()
        role_user = self.ref("container_accessibility.role_user")
        with self._mock_user_limit(current_count + 1):
            with patch(
                "odoo.addons.container_accessibility.models.res_users.ResUsers._check_user_limit_exceeded"
            ) as _check_user_limit_exceeded:
                new_user = self.env["res.users"].create(
                    {"name": "Test User", "login": "testuser", "role_id": role_user}
                )
                _check_user_limit_exceeded.assert_called()
            with patch(
                "odoo.addons.container_accessibility.models.res_users.ResUsers._check_user_limit_exceeded"
            ) as _check_user_limit_exceeded:
                new_user.groups_id = [
                    (4, self.ref("container_accessibility.group_restricted"))
                ]
                _check_user_limit_exceeded.assert_called()
            with self.assertRaisesRegex(UserError, "User limit exceeded"):
                self.env["res.users"].create(
                    {
                        "name": "Test User2",
                        "login": "testuser2",
                        "role_id": role_user,
                    }
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
