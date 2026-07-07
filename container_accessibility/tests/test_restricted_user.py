from odoo.addons.base.tests.common import BaseCommon


class TestRestrictedUser(BaseCommon):
    def setUp(self):
        super().setUp()

    def test_cannot_create_non_restricted_user(self):
        pass

    def test_change_itself_to_non_restricted_user(self):
        pass
